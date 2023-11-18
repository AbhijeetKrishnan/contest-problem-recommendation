from enum import Enum, auto
from typing import List, Optional

from pydantic import (BaseModel, Field, HttpUrl, NonNegativeFloat,
                      NonNegativeInt, PositiveFloat, PositiveInt, StrictInt)


class User(BaseModel):
    "Represents a Codeforces user."

    handle: str
    email: str
    vkId: str
    openId: str
    firstName: Optional[str]
    lastNam: Optional[str]
    country: Optional[str]
    city: Optional[str]
    organization: Optional[str]
    contribution: StrictInt
    rank: str
    rating: StrictInt
    maxRank: str
    maxRating: StrictInt
    lastOnlineTimeSeconds: NonNegativeInt
    registrationTimeSeconds: NonNegativeInt
    friendOfCount: NonNegativeInt
    avatar: HttpUrl
    titlePhoto: HttpUrl


class BlogEntry(BaseModel):
    "Represents a Codeforces blog entry. May be in either short or full version."

    id: int
    originalLocale: str
    creationTimeSeconds: NonNegativeInt
    authorHandle: str
    title: str
    content: str
    locale: str
    modificationTimeSeconds: NonNegativeInt
    allowViewHistory: bool
    tags: List[str]
    rating: StrictInt


class Comment(BaseModel):
    "Represents a comment."

    id: int
    creationTimeSeconds: NonNegativeInt
    commentatorHandle: str
    locale: str
    text: str
    parentCommentId: Optional[int]
    rating: NonNegativeInt


class RecentAction(BaseModel):
    "Represents a recent action."

    timeSeconds: NonNegativeInt
    blogEntry: BlogEntry
    comment: Comment


class RatingChange(BaseModel):
    "Represents a participation of user in rated contest."

    contestId: int
    contestName: str
    handle: str
    rank: PositiveInt
    ratingUpdateTimeSeconds: NonNegativeInt
    oldRating: NonNegativeInt
    newRating: NonNegativeInt


class ContestType(str, Enum):
    CF = 'CF'
    IOI = 'IOI'
    ICPC = 'ICPC'


class ContestPhase(str, Enum):
    BEFORE = 'BEFORE'
    CODING = 'CODING'
    PENDING_SYSTEM_TEST = 'PENDING_SYSTEM_TEST'
    SYSTEM_TEST = 'SYSTEM_TEST'
    FINISHED = 'FINISHED'


class Contest(BaseModel):
    "Represents a contest on Codeforces."

    id: int
    name: str
    type: ContestType
    phase: ContestPhase
    frozen: bool
    durationSeconds: NonNegativeInt
    startTimeSeconds: Optional[NonNegativeInt]
    relativeTimeSeconds: Optional[StrictInt]
    preparedBy: Optional[str]
    websiteUrl: Optional[HttpUrl]
    description: Optional[str]
    difficulty: Optional[int] = Field(ge=1, le=5)
    kind: Optional[str] = Field(
        pattern=r'Official ICPC Contest|Official School Contest|Opencup Contest|School/University/City/Region Championship|Training Camp Contest|Official International Personal Contest|Training Contest')
    icpcRegion: Optional[str]
    country: Optional[str]
    city: Optional[str]
    season: Optional[str]


class ParticipantType(str, Enum):
    CONTESTANT = 'CONTESTANT'
    PRACTICE = 'PRACTICE'
    VIRTUAL = 'VIRTUAL'
    MANAGER = 'MANAGER'
    OUT_OF_COMPETITION = 'OUT_OF_COMPETITION'


class Member(BaseModel):
    "Represents a member of a party."

    handle: str
    name: Optional[str]


class Party(BaseModel):
    "Represents a party, participating in a contest."

    contestId: Optional[int]
    members: List[Member]
    participantType: ParticipantType
    teamId: Optional[int]
    teamName: Optional[str]
    ghost: bool
    room: Optional[int]
    startTimeSeconds: Optional[NonNegativeInt]


class ProblemType(str, Enum):
    PROGRAMMING = 'PROGRAMMING'
    QUESTION = 'QUESTION'


class Problem(BaseModel):
    "Represents a problem."

    contestId: Optional[int]
    problemsetName: Optional[str]
    index: str
    name: str
    type: ProblemType
    points: Optional[PositiveFloat]
    rating: Optional[NonNegativeInt]
    tags: List[str]


class ProblemStatistics(BaseModel):
    "Represents a statistic data about a problem."

    contestId: Optional[int]
    index: str
    solvedCount: NonNegativeInt


class Verdict(str, Enum):
    FAILED = 'FAILED'
    OK = 'OK'
    PARTIAL = 'PARTIAL'
    COMPILATION_ERROR = 'COMPILATION_ERROR'
    RUNTIME_ERROR = 'RUNTIME_ERROR'
    WRONG_ANSWER = 'WRONG_ANSWER'
    PRESENTATION_ERROR = 'PRESENTATION_ERROR'
    TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED'
    MEMORY_LIMIT_EXCEEDED = 'MEMORY_LIMIT_EXCEEDED'
    IDLENESS_LIMIT_EXCEEDED = 'IDLENESS_LIMIT_EXCEEDED'
    SECURITY_VIOLATED = 'SECURITY_VIOLATED'
    CRASHED = 'CRASHED'
    INPUT_PREPARATION_CRASHED = 'INPUT_PREPARATION_CRASHED'
    CHALLENGED = 'CHALLENGED'
    SKIPPED = 'SKIPPED'
    TESTING = 'TESTING'
    REJECTED = 'REJECTED'


class TestSet(str, Enum):
    SAMPLES = 'SAMPLES'
    PRETESTS = 'PRETESTS'
    TESTS = 'TESTS'
    TESTS1 = 'TESTS1'
    TESTS2 = 'TESTS2'
    TESTS3 = 'TESTS3'
    TESTS4 = 'TESTS4'
    TESTS5 = 'TESTS5'
    TESTS6 = 'TESTS6'
    TESTS7 = 'TESTS7'
    TESTS8 = 'TESTS8'
    TESTS9 = 'TESTS9'
    TESTS10 = 'TESTS10'


class Submission(BaseModel):
    "Represents a submission."

    id: int
    contestId: Optional[int]
    creationTimeSeconds: Optional[NonNegativeInt]
    relativeTimeSeconds: int
    problem: Problem
    author: Party
    programmingLanguage: str
    verdict: Optional[Verdict]
    testset: TestSet
    passedTestCount: NonNegativeInt
    timeConsumedMillis: NonNegativeInt
    memoryConsumedBytes: NonNegativeInt
    points: Optional[NonNegativeFloat]


class HackVerdict(str, Enum):
    HACK_SUCCESSFUL = 'HACK_SUCCESSFUL'
    HACK_UNSUCCESSFUL = 'HACK_UNSUCCESSFUL'
    INVALID_INPUT = 'INVALID_INPUT'
    GENERATOR_INCOMPILABLE = 'GENERATOR_INCOMPILABLE'
    GENERATOR_CRASHED = 'GENERATOR_CRASHED'
    IGNORED = 'IGNORED'
    TESTING = 'TESTING'
    OTHER = 'OTHER'


class JudgeProtocol(BaseModel):
    manual: bool
    protocol: str
    verdict: HackVerdict


class Hack(BaseModel):
    "Represents a hack, made during Codeforces Round."

    id: int
    creationTimeSeconds: NonNegativeInt
    hacker: Party
    defender: Party
    verdict: Optional[HackVerdict]
    problem: Problem
    test: Optional[str]
    judgeProtocol: Optional[JudgeProtocol]


class ProblemResultType(str, Enum):
    PRELIMINARY = 'PRELIMINARY'
    FINAL = 'FINAL'


class ProblemResult(BaseModel):
    points: NonNegativeFloat
    penalty: Optional[int]
    rejectedAttemptCount: NonNegativeInt
    type: ProblemResultType
    bestSubmissionTimeSeconds: Optional[NonNegativeInt]


class RanklistRow(BaseModel):
    party: Party
    rank: PositiveInt
    points: NonNegativeFloat
    penalty: int
    successfulHackCount: NonNegativeInt
    unsuccessfulHackCount: NonNegativeInt
    problemResults: List[ProblemResult]
    lastSubmissionTimeSeconds: Optional[NonNegativeInt]
