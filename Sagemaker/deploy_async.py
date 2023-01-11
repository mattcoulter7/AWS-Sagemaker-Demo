from sagemaker.huggingface import HuggingFaceModel
from sagemaker.async_inference.async_inference_config import AsyncInferenceConfig
from sagemaker.s3 import s3_path_join
import sagemaker

sess = sagemaker.Session()
role = sagemaker.get_execution_role()
s3_bucket = sess.default_bucket()

# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'valhalla/t5-base-e2e-qg',
	'HF_TASK':'text2text-generation'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	transformers_version='4.17.0',
	pytorch_version='1.10.2',
	py_version='py38',
	env=hub,
	role=role, 
)

async_config = AsyncInferenceConfig(
    output_path=s3_path_join("s3://",s3_bucket,"async_inference/output"),
    # notification_config={
            #   "SuccessTopic": "arn:aws:sns:us-east-2:123456789012:MyTopic",
            #   "ErrorTopic": "arn:aws:sns:us-east-2:123456789012:MyTopic",
    # }, #  Notification configuration
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1, # number of instances
	instance_type='ml.m5.xlarge', # ec2 instance type
    async_inference_config=async_config
)

output = predictor.predict({
	'inputs': "Python is a programming language. It is developed by Guido Van Rossum and released in 1991. </s>"
})
print(output)