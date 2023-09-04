"""Implement sklearn linear model."""
from typing import Any, Dict

import sklearn.linear_model

from .base import SklearnKNeighborsClassifierMixin


# pylint: disable=invalid-name,too-many-instance-attributes
class KNeighborsClassifier(SklearnKNeighborsClassifierMixin):
    """A k-nearest classifier model with FHE.

    Parameters:
        n_bits (int, Dict[str, int]): Number of bits to quantize the model. If an int is passed
            for n_bits, the value will be used for quantizing inputs and weights. If a dict is
            passed, then it should contain "op_inputs" and "op_weights" as keys with
            corresponding number of quantization bits so that:
            - op_inputs : number of bits to quantize the input values
            - op_weights: number of bits to quantize the learned parameters
            Default to 8.

    For more details on KNeighborsClassifier please refer to the scikit-learn documentation:
    https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    """

    sklearn_model_class = sklearn.neighbors.KNeighborsClassifier
    _is_a_public_cml_model = True

    def __init__(
        self,
        n_bits=8,
        n_neighbors=5,
        *,
        weights="uniform",
        algorithm="auto",
        leaf_size=30,
        p=2,
        metric="minkowski",
        metric_params=None,
        n_jobs=None,
    ):
        # Call SklearnKNeighborsClassifierMixin's __init__ method
        super().__init__(n_bits=n_bits)

        self.n_neighbors = n_neighbors
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.p = p
        self.metric = metric
        self.metric_params = metric_params
        self.n_jobs = n_jobs
        self.weights = weights

    def dump_dict(self) -> Dict[str, Any]:
        assert self._weight_quantizer is not None, self._is_not_fitted_error_message()

        metadata: Dict[str, Any] = {}

        # Concrete ML
        metadata["n_bits"] = self.n_bits
        metadata["sklearn_model"] = self.sklearn_model
        metadata["_is_fitted"] = self._is_fitted
        metadata["_is_compiled"] = self._is_compiled
        metadata["input_quantizers"] = self.input_quantizers
        metadata["_weight_quantizer"] = self._weight_quantizer
        metadata["_q_X_fit_quantizer"] = self._q_X_fit_quantizer
        metadata["_q_X_fit"] = self._q_X_fit

        metadata["output_quantizers"] = self.output_quantizers
        metadata["onnx_model_"] = self.onnx_model_
        metadata["post_processing_params"] = self.post_processing_params
        metadata["cml_dumped_class_name"] = type(self).__name__

        # Scikit-learn
        metadata["sklearn_model_class"] = self.sklearn_model_class
        metadata["n_neighbors"] = self.n_neighbors
        metadata["algorithm"] = self.algorithm
        metadata["weights"] = self.weights
        metadata["leaf_size"] = self.leaf_size
        metadata["p"] = self.p
        metadata["metric"] = self.metric
        metadata["metric_params"] = self.metric_params
        metadata["n_jobs"] = self.n_jobs

        return metadata

    @classmethod
    def load_dict(cls, metadata: Dict):

        # Instantiate the model
        obj = KNeighborsClassifier()

        # Concrete-ML
        obj.n_bits = metadata["n_bits"]
        obj.sklearn_model = metadata["sklearn_model"]
        obj._is_fitted = metadata["_is_fitted"]
        obj._is_compiled = metadata["_is_compiled"]
        obj.input_quantizers = metadata["input_quantizers"]
        obj.output_quantizers = metadata["output_quantizers"]
        obj._weight_quantizer = metadata["_weight_quantizer"]
        obj._q_X_fit_quantizer = metadata["_q_X_fit_quantizer"]
        obj._q_X_fit = metadata["_q_X_fit"]

        obj.onnx_model_ = metadata["onnx_model_"]

        obj.post_processing_params = metadata["post_processing_params"]

        # Scikit-Learn
        obj.n_neighbors = metadata["n_neighbors"]
        obj.weights = metadata["weights"]
        obj.algorithm = metadata["algorithm"]
        obj.p = metadata["p"]
        obj.metric = metadata["metric"]
        obj.metric_params = metadata["metric_params"]
        obj.n_jobs = metadata["n_jobs"]
        return obj