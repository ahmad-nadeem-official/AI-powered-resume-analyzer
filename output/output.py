from typing import Literal
from pydantic import BaseModel, Field


class OP(BaseModel):

    is_resume: bool = Field(
        description="Whether the uploaded file is a valid resume or CV."
    )

    name: str | None = Field(
        default=None,
        description="Full name of the candidate. Return it in lowercase. Return null if it cannot be reliably identified."
    )

    phone: str | None = Field(
        default=None,
        description="Candidate's phone number exactly as written in the resume. Preserve country code and formatting. Return null only if no phone number is present."
    )

    email: str | None = Field(
        default=None,
        description="Candidate's email address. Return it in lowercase. Return null if it cannot be found."
    )

    score: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Job match score from 0 to 100 based only on documented alignment between the resume and job description."
    )

    wrong_file_reason: str | None = Field(
        default=None,
        description="If the uploaded file is not a resume, explain why. Otherwise return null."
    )