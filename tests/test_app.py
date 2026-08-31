from streamlit.testing.v1 import AppTest


def test_demo_workflow_analysis_approval_and_reset(monkeypatch):
    monkeypatch.setenv("APP_DEMO_MODE", "true")
    app = AppTest.from_file("../app.py", default_timeout=10).run()
    assert not app.exception
    assert "Preview mode" in app.info[0].value

    app.button(key="analyse").click().run()
    assert not app.exception
    assert any("Incident brief" in heading.value for heading in app.subheader)
    assert app.button(key="approve")

    app.button(key="approve").click().run()
    assert not app.exception
    assert any("Approved at" in message.value for message in app.success)

    app.button(key="reset").click().run()
    assert not app.exception
    assert not any("Incident brief" in heading.value for heading in app.subheader)


def test_empty_incident_shows_validation_error(monkeypatch):
    monkeypatch.setenv("APP_DEMO_MODE", "true")
    app = AppTest.from_file("../app.py", default_timeout=10).run()
    app.text_area(key="incident_text").set_value("")
    app.button(key="analyse").click().run()
    assert not app.exception
    assert "Enter an incident description" in app.error[0].value
