from typing import Optional

def setup_tracing(service_name: str = "capstone-api") -> Optional[object]:
	try:
		from opentelemetry import trace
		from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
		from opentelemetry.sdk.resources import Resource
		from opentelemetry.sdk.trace import TracerProvider
		from opentelemetry.sdk.trace.export import BatchSpanProcessor
		resource = Resource.create({"service.name": service_name})
		provider = TracerProvider(resource=resource)
		exporter = OTLPSpanExporter()
		processor = BatchSpanProcessor(exporter)
		provider.add_span_processor(processor)
		trace.set_tracer_provider(provider)
		return provider
	except Exception:
		return None