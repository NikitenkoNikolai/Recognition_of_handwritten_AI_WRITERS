import tensorflow as tf

class CTC(tf.keras.losses.Loss):

  def __init__(self, name:str = None) -> None:
      super().__init__(name = name)
      self.loss_fn = tf.keras.backend.ctc_batch_cost

  def __call__(self, y_true, y_pred) -> tf.Tensor:
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    loss = self.loss_fn(y_true, y_pred, input_length, label_length)
    return loss