# -*- coding:utf-8 -*-
import copy
import json
import logging
import os
import sys
from io import open

logger = logging.getLogger(__name__)

CONFIG_NAME = "config.json"


class PretrainedConfig(object):
    pretrained_config_archive_map = {}

    def __init__(self, **kwargs):
        pass

    def save_pretrained(self, save_directory):
        """ Save a configuration object to the directory `save_directory`, so that it
            can be re-loaded using the :func:`~transformers.PretrainedConfig.from_pretrained` class method.
        """
        assert os.path.isdir(
            save_directory), "Saving path should be a directory where the model and configuration can be saved"

        # If we save using the predefined names, we can load using `from_pretrained`
        output_config_file = os.path.join(save_directory, CONFIG_NAME)

        self.to_json_file(output_config_file)
        logger.info("Configuration saved in {}".format(output_config_file))

    @classmethod
    def from_pretrained(cls, pretrained_path, **kwargs):

        json_file = os.path.join(pretrained_path)

        # Load config
        config = cls.from_json_file(json_file)

        # Update config with kwargs if needed
        for key, value in kwargs.items():
            setattr(config, key, value)

        logger.info("Model config %s", config)
        return config

    @classmethod
    def from_dict(cls, json_object):
        """Constructs a `Config` from a Python dictionary of parameters."""
        config = cls(vocab_size_or_config_json_file=-1)
        for key, value in json_object.items():
            setattr(config, key, value)
        return config

    @classmethod
    def from_json_file(cls, json_file):
        """Constructs a `BertConfig` from a json file of parameters."""
        with open(json_file, "r", encoding='utf-8') as reader:
            text = reader.read()
        return cls.from_dict(json.loads(text))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.to_json_string())

    def to_dict(self):
        """Serializes this instance to a Python dictionary."""
        output = copy.deepcopy(self.__dict__)
        return output

    def to_json_string(self):
        """Serializes this instance to a JSON string."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"

    def to_json_file(self, json_file_path):
        """ Save this instance to a json file."""
        with open(json_file_path, "w", encoding='utf-8') as writer:
            writer.write(self.to_json_string())


class BertConfig(PretrainedConfig):
    r"""
        :class:`~transformers.BertConfig` is the configuration class to store the configuration of a
        `BertModel`.


        Arguments:
            vocab_size_or_config_json_file: Vocabulary size of `inputs_ids` in `BertModel`.
            hidden_size: Size of the encoder layers and the pooler layer.
            num_hidden_layers: Number of hidden layers in the Transformer encoder.
            num_attention_heads: Number of attention heads for each attention layer in
                the Transformer encoder.
            intermediate_size: The size of the "intermediate" (i.e., feed-forward)
                layer in the Transformer encoder.
            hidden_act: The non-linear activation function (function or string) in the
                encoder and pooler. If string, "gelu", "relu", "swish" and "gelu_new" are supported.
            hidden_dropout_prob: The dropout probabilitiy for all fully connected
                layers in the embeddings, encoder, and pooler.
            attention_probs_dropout_prob: The dropout ratio for the attention
                probabilities.
            max_position_embeddings: The maximum sequence length that this model might
                ever be used with. Typically set this to something large just in case
                (e.g., 512 or 1024 or 2048).
            type_vocab_size: The vocabulary size of the `token_type_ids` passed into
                `BertModel`.
            initializer_range: The sttdev of the truncated_normal_initializer for
                initializing all weight matrices.
            layer_norm_eps: The epsilon used by LayerNorm.
    """

    def __init__(self,
                 vocab_size_or_config_json_file=21128,
                 hidden_size=768,
                 num_hidden_layers=12,
                 num_attention_heads=12,
                 intermediate_size=3072,
                 hidden_act="gelu",
                 hidden_dropout_prob=0.1,
                 attention_probs_dropout_prob=0.1,
                 max_position_embeddings=512,
                 type_vocab_size=2,
                 initializer_range=0.02,
                 layer_norm_eps=1e-12,
                 **kwargs):
        super(BertConfig, self).__init__(**kwargs)
        if isinstance(vocab_size_or_config_json_file, str) or (sys.version_info[0] == 2
                                                               and isinstance(vocab_size_or_config_json_file, unicode)):
            with open(vocab_size_or_config_json_file, "r", encoding='utf-8') as reader:
                json_config = json.loads(reader.read())
            for key, value in json_config.items():
                self.__dict__[key] = value
        elif isinstance(vocab_size_or_config_json_file, int):
            self.vocab_size = vocab_size_or_config_json_file
            self.hidden_size = hidden_size
            self.num_hidden_layers = num_hidden_layers
            self.num_attention_heads = num_attention_heads
            self.hidden_act = hidden_act
            self.intermediate_size = intermediate_size
            self.hidden_dropout_prob = hidden_dropout_prob
            self.attention_probs_dropout_prob = attention_probs_dropout_prob
            self.max_position_embeddings = max_position_embeddings
            self.type_vocab_size = type_vocab_size
            self.initializer_range = initializer_range
            self.layer_norm_eps = layer_norm_eps
        else:
            raise ValueError("First argument must be either a vocabulary size (int)"
                             " or the path to a pretrained model config file (str)")


class DistillBertConfig(PretrainedConfig):
    r"""
       Arguments:
           vocab_size_or_config_json_file: Vocabulary size of `inputs_ids` in `BertModel`.
           hidden_size: Size of the encoder layers and the pooler layer.
           num_hidden_layers: Number of hidden layers in the Transformer encoder.
           num_attention_heads: Number of attention heads for each attention layer in
               the Transformer encoder.
           intermediate_size: The size of the "intermediate" (i.e., feed-forward)
               layer in the Transformer encoder.
           hidden_act: The non-linear activation function (function or string) in the
               encoder and pooler. If string, "gelu", "relu", "swish" and "gelu_new" are supported.
           hidden_dropout_prob: The dropout probabilitiy for all fully connected
               layers in the embeddings, encoder, and pooler.
           attention_probs_dropout_prob: The dropout ratio for the attention
               probabilities.
           max_position_embeddings: The maximum sequence length that this model might
               ever be used with. Typically set this to something large just in case
               (e.g., 512 or 1024 or 2048).
           initializer_range: The sttdev of the truncated_normal_initializer for
               initializing all weight matrices.
           layer_norm_eps: The epsilon used by LayerNorm.
   """

    def __init__(self,
                 vocab_size_or_config_json_file=21128,
                 hidden_size=768,
                 num_hidden_layers=6,
                 num_attention_heads=12,
                 intermediate_size=3072,
                 hidden_act="gelu",
                 hidden_dropout_prob=0.1,
                 attention_probs_dropout_prob=0.1,
                 max_position_embeddings=512,
                 initializer_range=0.02,
                 layer_norm_eps=1e-12,
                 sequence_classif_dropout_prob=0.2,
                 **kwargs):
        super(DistillBertConfig, self).__init__(**kwargs)
        if isinstance(vocab_size_or_config_json_file, str) or (sys.version_info[0] == 2
                                                               and isinstance(vocab_size_or_config_json_file, unicode)):
            with open(vocab_size_or_config_json_file, "r", encoding='utf-8') as reader:
                json_config = json.loads(reader.read())
            for key, value in json_config.items():
                self.__dict__[key] = value
        elif isinstance(vocab_size_or_config_json_file, int):
            self.vocab_size = vocab_size_or_config_json_file
            self.hidden_size = hidden_size
            self.num_hidden_layers = num_hidden_layers
            self.num_attention_heads = num_attention_heads
            self.hidden_act = hidden_act
            self.intermediate_size = intermediate_size
            self.hidden_dropout_prob = hidden_dropout_prob
            self.attention_probs_dropout_prob = attention_probs_dropout_prob
            self.max_position_embeddings = max_position_embeddings
            self.initializer_range = initializer_range
            self.layer_norm_eps = layer_norm_eps
            self.sequence_classif_dropout_prob = sequence_classif_dropout_prob

        else:
            raise ValueError("First argument must be either a vocabulary size (int)"
                             " or the path to a pretrained model config file (str)")


class ALBertConfig(PretrainedConfig):
    r"""Constructs AlbertConfig.

    Args:
        vocab_size_or_config_json_file: Vocabulary size of `inputs_ids` in `BertModel`.
        hidden_size: Size of the encoder layers and the pooler layer.
        num_hidden_layers: Number of hidden layers in the Transformer encoder.
        num_hidden_groups: Number of group for the hidden layers, parameters in
            the same group are shared.
        num_attention_heads: Number of attention heads for each attention layer in
            the Transformer encoder.
        intermediate_size: The size of the "intermediate" (i.e., feed-forward)
            layer in the Transformer encoder.
        inner_group_num: int, number of inner repetition of attention and ffn.
        down_scale_factor: float, the scale to apply
        hidden_act: The non-linear activation function (function or string) in the
            encoder and pooler. If string, "gelu", "relu", "swish" and "gelu_new" are supported.
        hidden_dropout_prob: The dropout probabilitiy for all fully connected
            layers in the embeddings, encoder, and pooler.
        attention_probs_dropout_prob: The dropout ratio for the attention
            probabilities.
        max_position_embeddings: The maximum sequence length that this model might
            ever be used with. Typically set this to something large just in case
            (e.g., 512 or 1024 or 2048).
        type_vocab_size: The vocabulary size of the `token_type_ids` passed into
            `BertModel`.
        initializer_range: The sttdev of the truncated_normal_initializer for
            initializing all weight matrices.
        layer_norm_eps: The epsilon used by LayerNorm.
    """

    def __init__(self,
                 vocab_size_or_config_json_file=21128,
                 embedding_size=128,
                 hidden_size=768,
                 num_hidden_layers=12,
                 num_hidden_groups=1,
                 num_attention_heads=64,
                 intermediate_size=16384,
                 inner_group_num=1,
                 hidden_act="gelu",
                 hidden_dropout_prob=0.1,
                 attention_probs_dropout_prob=0.1,
                 max_position_embeddings=512,
                 type_vocab_size=2,
                 initializer_range=0.02,
                 layer_norm_eps=1e-12,
                 **kwargs):
        super(ALBertConfig, self).__init__(**kwargs)
        if isinstance(vocab_size_or_config_json_file, str) or (sys.version_info[0] == 2
                                                               and isinstance(vocab_size_or_config_json_file, unicode)):
            with open(vocab_size_or_config_json_file, "r", encoding='utf-8') as reader:
                json_config = json.loads(reader.read())
            for key, value in json_config.items():
                self.__dict__[key] = value
        elif isinstance(vocab_size_or_config_json_file, int):
            self.vocab_size = vocab_size_or_config_json_file
            self.embedding_size = embedding_size
            self.hidden_size = hidden_size
            self.num_hidden_layers = num_hidden_layers
            self.num_hidden_groups = num_hidden_groups
            self.num_attention_heads = num_attention_heads
            self.inner_group_num = inner_group_num
            self.hidden_act = hidden_act
            self.intermediate_size = intermediate_size
            self.hidden_dropout_prob = hidden_dropout_prob
            self.attention_probs_dropout_prob = attention_probs_dropout_prob
            self.max_position_embeddings = max_position_embeddings
            self.type_vocab_size = type_vocab_size
            self.initializer_range = initializer_range
            self.layer_norm_eps = layer_norm_eps
        else:
            raise ValueError("First argument must be either a vocabulary size (int)"
                             " or the path to a pretrained model config file (str)")
