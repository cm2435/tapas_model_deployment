import logging
import os
import sys
import time
from abc import abstractmethod
from pathlib import Path
from posixpath import split
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import torch
import torch.nn as nn
import uvicorn
import yaml
from scipy.spatial.distance import cosine
from transformers import (
    RobertaConfig,
    RobertaModel,
    RobertaTokenizer,
    TapasConfig,
    TapasForQuestionAnswering,
    TapasTokenizer,
)


class InferenceModel(object):
    """Class for an ML API providing inference using a pre-trained model."""

    def __init__(self):
        """
        Initializes the InferenceModel.

        - Sets the device to GPU if available, else CPU.
        - Loads model configuration and arguments from config.yaml file.
        - Initializes tokenizer, config, and model.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.config_path = Path(__file__).parent / "config.yaml"
        self.model_args = yaml.safe_load(self.config_path.read_text())
        self.serving_args = self.model_args["qa_model"]["inference"]

        self.tokenizer = TapasTokenizer.from_pretrained(
            self.model_args["qa_model"]["base_model"]
        )
        self.config = TapasConfig.from_pretrained(
            self.model_args["qa_model"]["base_model"]
        )
        self.model = self.load_model()

    @staticmethod
    def batch_questions(questions: List[str], batch_size: int):
        """
        Batches questions into smaller lists based on the given batch size.

        Args:
            questions: A list of strings representing the questions.
            batch_size: An integer representing the batch size.

        Returns:
            A nested list of strings representing the batched questions.
        """
        nested_list = []
        for i in range(0, len(questions), batch_size):
            nested_list.append(questions[i : i + batch_size])
        return nested_list

    def load_model(self):
        """
        Loads the pre-trained TapasForQuestionAnswering model.

        - Loads the model with torch.jit.trace() and extracts input tensors for torchscripting.
        - Torchscripts the model using the extracted tensors.
        - Prints model loading time.

        Returns:
            The torchscripted model.
        """
        start = time.time()
        model = TapasForQuestionAnswering.from_pretrained(
            self.model_args["qa_model"]["base_model"], torchscript=True
        ).to(self.device)

        # Script the model on device so do not need to worry about version mismatches in CUDA etc.
        # This is a dummy example
        data = {
            "Actors": ["Brad Pitt", "Leonardo Di Caprio", "George Clooney"],
            "Number of movies": ["87", "53", "69"],
        }
        queries = ["What is the name of the first actor?"]
        table = pd.DataFrame.from_dict(data)
        inputs = self.tokenizer(
            table=table, queries=queries, padding="max_length", return_tensors="pt"
        )
        for key in inputs.keys():
            inputs[key] = inputs[key].to(self.device)

        # Torchscript the model using the extracted tensors
        traced_model = torch.jit.trace(
            model.forward,
            (inputs.input_ids, inputs.attention_mask, inputs.token_type_ids),
        )
        print(
            "Search retrieval model for task: question_answering loaded correctly to device {} in {} seconds".format(
                self.device, time.time() - start
            )
        )
        return traced_model

    def tokenize(
        self,
        table: pd.DataFrame,
        queries: List[str],
        padding: str = "max_length",
        tensor_return_type: str = "pt",
    ) -> list:
        """
        Tokenizes table and queries.

        Args:
            table: A Pandas DataFrame representing the table.
            queries: A list of strings representing the queries.
            padding: The padding strategy. Defaults to "max_length".
            tensor_return_type: The type of tensors to return. Defaults to "pt".

        Returns:
            The tokenized inputs.
        """
        return self.tokenizer(
            table=table,
            queries=queries,
            padding=padding,
            return_tensors=tensor_return_type,
        )

    def make_inference_minibatch(
        self,
        question_batch: Union[list, str],
        table: pd.DataFrame,
    ) -> list:
        """
        Makes inference on a minibatch of questions and a table.

        Args:
            question_batch: A list or string representing the questions.
            table: A Pandas DataFrame representing the table.

        Returns:
            A list of dictionaries representing the inference results.
        """
        start = time.time()
        inputs = self.tokenize(
            table=table,
            queries=question_batch,
        ).to(self.device)
        answers = []
        with torch.inference_mode(), torch.cuda.amp.autocast():
            output = self.model(**inputs)

        print(
            f"inference_logged- table_length:{len(table)}, num_questions:{len(question_batch)}, inference_time:{time.time()-start:.4f}, average_inference_time:{((time.time()-start) / len(question_batch)):.4f}"
        )

        (
            predicted_answer_coordinates,
            predicted_aggregation_indices,
        ) = self.tokenizer.convert_logits_to_predictions(
            inputs.to("cpu"), output[0].cpu().detach(), output[1].cpu().detach()
        )
        for coordinates in predicted_answer_coordinates:
            if len(coordinates) == 1:
                # only a single cell
                answers.append(table.iat[coordinates[0]])
            else:
                # multiple cells
                cell_values = []
                for coordinate in coordinates:
                    cell_values.append(table.iat[coordinate])
                answers.append(", ".join(cell_values))

        id2aggregation = {0: "NONE", 1: "SUM", 2: "AVERAGE", 3: "COUNT"}
        aggregation_predictions_string = [
            id2aggregation[x] for x in predicted_aggregation_indices
        ]

        response_list = []
        for query, answer, predicted_agg in zip(
            question_batch, answers, aggregation_predictions_string
        ):
            result = {
                "question": query,
                "answer": answer,
                "predicted_aggregation": predicted_agg,
            }
            response_list.append(result)
        return response_list

    def inference(
        self,
        questions: Union[List[str], str],
        table: Dict[str, List[str]],
    ) -> dict:
        """
        Performs inference on a list of questions with a table.

        Args:
            questions: A list or string representing the questions.
            table: A dictionary representing the table.

        Returns:
            A dictionary representing the final inference results.
        """
        final_inferences = []
        batched_questions = self.batch_questions(
            questions, batch_size=self.serving_args["batch_size"]
        )
        for batch in batched_questions:
            inference = self.make_inference_minibatch(
                question_batch=batch,
                table=table,
            )
            final_inferences.extend(inference)

        return final_inferences
