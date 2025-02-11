"""
Example tests for the cognitive processor component.
"""
import pytest
import numpy as np
from cognitive_framework.processor import CognitiveProcessor
from cognitive_framework.types import ProcessingResult

def test_processor_initialization(model_config):
    """Test processor initialization with configuration."""
    processor = CognitiveProcessor(model_config)
    assert processor.config.layers == model_config["layers"]
    assert processor.config.activation == model_config["activation"]

@pytest.mark.parametrize("input_data,expected_shape", [
    (np.random.randn(10, 64), (10, 16)),
    (np.random.randn(1, 64), (1, 16)),
])
def test_processor_forward_pass(model_config, input_data, expected_shape):
    """Test processor forward pass with different input shapes."""
    processor = CognitiveProcessor(model_config)
    result = processor.process(input_data)
    assert isinstance(result, ProcessingResult)
    assert result.output.shape == expected_shape

@pytest.mark.asyncio
async def test_processor_async_processing(model_config, temp_workspace):
    """Test asynchronous processing capabilities."""
    processor = CognitiveProcessor(model_config)
    input_data = np.random.randn(5, 64)

    async def process_batch():
        return await processor.process_async(input_data)

    result = await process_batch()
    assert result.success
    assert result.processing_time > 0

def test_processor_error_handling(model_config):
    """Test error handling with invalid inputs."""
    processor = CognitiveProcessor(model_config)

    with pytest.raises(ValueError, match="Invalid input shape"):
        processor.process(np.random.randn(10, 32))  # Wrong input dimension

def test_processor_state_management(model_config):
    """Test processor state management and persistence."""
    processor = CognitiveProcessor(model_config)

    # Set internal state
    processor.set_state({"temperature": 0.7, "top_k": 10})

    # Process with state
    result = processor.process(
        np.random.randn(1, 64),
        use_state=True
    )

    assert result.state["temperature"] == 0.7
    assert result.state["top_k"] == 10

@pytest.mark.integration
def test_processor_pipeline_integration(model_config, temp_workspace):
    """Integration test for full processing pipeline."""
    from cognitive_framework.pipeline import ProcessingPipeline

    processor = CognitiveProcessor(model_config)
    pipeline = ProcessingPipeline([
        ("preprocessor", "StandardPreprocessor"),
        ("processor", processor),
        ("postprocessor", "StandardPostprocessor")
    ])

    input_data = np.random.randn(10, 64)
    result = pipeline.run(input_data)

    assert result.success
    assert len(result.pipeline_stages) == 3
    assert all(stage.success for stage in result.pipeline_stages)

@pytest.mark.benchmark
def test_processor_performance(model_config, benchmark):
    """Benchmark test for processing performance."""
    processor = CognitiveProcessor(model_config)
    input_data = np.random.randn(100, 64)

    def process_batch():
        return processor.process(input_data)

    result = benchmark(process_batch)
    assert result.stats.mean < 0.1  # Processing should take less than 100ms
```
