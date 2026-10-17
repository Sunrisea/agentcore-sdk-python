"""Keep framework extras limited to the adapter's own dependencies."""

from importlib.metadata import requires

from packaging.requirements import Requirement


def test_google_adk_does_not_enable_unrelated_extensions():
    requirements = [Requirement(value) for value in requires("alibabacloud-agentcore-sdk") or []]
    adk = next(requirement for requirement in requirements if requirement.name == "google-adk")
    assert adk.marker is not None and adk.marker.evaluate({"extra": "google-adk"})
    assert not adk.extras

    # The model adapter needs LiteLLM, which the base SDK already provides.
    assert any(
        requirement.name == "litellm"
        and (requirement.marker is None or requirement.marker.evaluate({"extra": ""}))
        for requirement in requirements
    )
