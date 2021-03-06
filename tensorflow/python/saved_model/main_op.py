# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""SavedModel main op.

Builds a main op that defines the sequence of ops to be run as part of the
SavedModel load/restore operations.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from tensorflow.python.framework import ops
from tensorflow.python.ops import data_flow_ops as tf_data_flow_ops
from tensorflow.python.ops import variables as tf_variables


def main_op():
  """Returns a main op to init variables and tables.

  Returns the main op including the group of ops that initializes all
  variables, initializes local variables and initialize all tables.

  Returns:
    The set of ops to be run as part of the main op upon the load operation.
  """
  init = tf_variables.initialize_all_variables()
  init_local = tf_variables.initialize_local_variables()
  init_tables = tf_data_flow_ops.initialize_all_tables()
  return tf.group(init, init_local, init_tables)


def main_op_with_restore(restore_op_name):
  """Returns a main op to init variables, tables and restore the graph.

  Returns the main op including the group of ops that initializes all
  variables, initialize local variables, initialize all tables and the restore
  op name.

  Args:
    restore_op_name: Name of the op to use to restore the graph.

  Returns:
    The set of ops to be run as part of the main op upon the load operation.
  """
  simple_main_op = main_op()
  with ops.control_dependency([simple_main_op]):
    restore = restore_op_name
  return tf.group(restore)
