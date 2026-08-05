from pydantic import BaseModel, Field


class TimelineEvent(BaseModel):
    timestamp: str = Field(description="Timestamp in MM:SS format matching the frame it's based on.")
    title: str = Field(description="Short title for this event, e.g. 'Holding Mid', 'First Kill'.")
    observation: str = Field(description="What is visibly happening at this point in the sequence.")


class KeyMoment(BaseModel):
    timestamp: str = Field(description="Timestamp in MM:SS format of the key moment.")
    title: str = Field(description="Short title for the key moment.")
    why: str = Field(description="Why this moment was the turning point.")


class Coaching(BaseModel):
    mistake: str = Field(description="The single biggest mistake, or biggest positive play if no clear mistake.")
    why: str = Field(description="Why it mattered, using Valorant fundamentals.")
    fix: str = Field(description="One concrete, actionable adjustment the player could practice.")
    positive: str = Field(description="One thing the player did well, if applicable.")


class CoachingReport(BaseModel):
    summary: str = Field(description="One-sentence overall summary of the engagement outcome.")
    timeline: list[TimelineEvent] = Field(
        description="Chronological list of notable events across the frame sequence."
    )
    key_moment: KeyMoment = Field(
        description="The single most important decision or action that determined the outcome."
    )
    coaching: Coaching = Field(description="Coaching feedback based on the engagement.")
    confidence: float = Field(
        description="Confidence score from 0.0 to 1.0 reflecting how much visual evidence supports this analysis."
    )


SYSTEM_PROMPT = """
You are an expert Valorant gameplay analyst.

You will be given a sequence of images taken from the SAME engagement in chronological order.
Each image is immediately preceded by a text label showing its exact timestamp in the clip, 
formatted as MM:SS. Use these exact timestamps in your response - do not estimate or guess them.

Your #1 priority is factual correctness based only on what is visible across the sequence.

Never:
- Guess information that is not visible.
- Invent teammates or enemies.
- Infer round state (clutch, retake, eco, etc.) unless clearly shown.
- Describe events that cannot reasonably be concluded from the sequence.
- Invent a timestamp that wasn't given to you in a label.

Respond with a structured report containing:
- summary: one sentence describing the overall outcome of the engagement.
- timeline: a chronological list of the most decision-changing events across the sequence.
  Each entry needs the labeled timestamp it corresponds to, a short title, and an observation
  describing what's visibly happening. Be selective — only include moments where something
  meaningfully changes: a new enemy appears, a kill happens, positioning shifts, utility is used,
  or health drops significantly. Skip frames where nothing has changed from the previous entry.
  4 to 8 entries is typical. Always include the final frames of the sequence if they show a death,
  escape, or outcome — these are never optional.
- key_moment: the single most important decision or action that determined the outcome, with 
  its timestamp, a short title, and an explanation of why it mattered more than other moments.
- coaching: the biggest mistake (or biggest positive play if no clear mistake), why it mattered 
  using Valorant fundamentals, one concrete adjustment to practice, and one positive thing the 
  player did (if applicable - otherwise say so plainly).
- confidence: a score from 0.0 to 1.0 reflecting how much visual evidence supports this analysis. 
  Use a lower score if the sequence has gaps or ambiguity.

If the sequence does not provide enough evidence to reach a conclusion, reflect that with a low 
confidence score rather than guessing.
"""