# Data structures for cognitive framework analysis


@value
struct Concept:
    var id: Int
    var name: String
    var relevant_input_excerpt: String

    fn __init__(inout self, id: Int, name: String, excerpt: String):
        self.id = id
        self.name = name
        self.relevant_input_excerpt = excerpt


@value
struct Perspective:
    var name: String
    var validity: String
    var rating: Int
    var explanation: String

    fn __init__(
        inout self,
        name: String,
        validity: String,
        rating: Int,
        explanation: String,
    ):
        self.name = name
        self.validity = validity
        self.rating = rating
        self.explanation = explanation


@value
struct Connection:
    var concepts: List[String]
    var relationship: String
    var description: String

    fn __init__(
        inout self,
        concepts: List[String],
        relationship: String,
        description: String,
    ):
        self.concepts = concepts
        self.relationship = relationship
        self.description = description


@value
struct Pattern:
    var description: String

    fn __init__(inout self, description: String):
        self.description = description


@value
struct Assumption:
    var statement: String
    var counter_argument: String

    fn __init__(inout self, statement: String, counter_argument: String):
        self.statement = statement
        self.counter_argument = counter_argument


@value
struct Marker:
    var name: String
    var description: String
    var significance: String?

    fn __init__(
        inout self,
        name: String,
        description: String,
        significance: String? = None,
    ):
        self.name = name
        self.description = description
        self.significance = significance


@value
struct StageAnalysisItem:
    var title: String
    var concepts: List[Concept]?
    var perspectives: List[Perspective]?
    var connections: List[Connection]?
    var patterns: List[Pattern]?
    var assumptions: List[Assumption]?
    var markers: List[Marker]?
    var summary: String?

    fn __init__(
        inout self,
        title: String,
        concepts: List[Concept]? = None,
        perspectives: List[Perspective]? = None,
        connections: List[Connection]? = None,
        patterns: List[Pattern]? = None,
        assumptions: List[Assumption]? = None,
        markers: List[Marker]? = None,
        summary: String? = None,
    ):
        self.title = title
        self.concepts = concepts
        self.perspectives = perspectives
        self.connections = connections
        self.patterns = patterns
        self.assumptions = assumptions
        self.markers = markers
        self.summary = summary


@value
struct EmergentFramework:
    var title: String
    var components: List[Component]
    var summary: String

    fn __init__(
        inout self,
        title: String,
        components: List[Component],
        summary: String
    ):
        self.title = title
        self.components = components
        self.summary = summary


@value
struct Component:
    var name: String
    var description: String

    fn __init__(inout self, name: String, description: String):
        self.name = name
        self.description = description


@value
struct MojoCodeExample:
    var title: String
    var description: String
    var code: String

    fn __init__(inout self, title: String, description: String, code: String):
        self.title = title
        self.description = description
        self.code = code


@value
struct LowLevelUtilization:
    var low_level_mechanics: String
    var performance_enhancements: String
    var security_considerations: String

    fn __init__(
        inout self,
        mechanics: String,
        performance: String,
        security: String
    ):
        self.low_level_mechanics = mechanics
        self.performance_enhancements = performance
        self.security_considerations = security


@value
struct AnalysisResult:
    var stage_analysis: List[StageAnalysisItem]
    var emergent_framework: EmergentFramework
    var mojo_code_example_1: MojoCodeExample
    var low_level_utilization_1: LowLevelUtilization
    var mojo_code_example_2: MojoCodeExample
    var low_level_utilization_2: LowLevelUtilization
    var conclusion: String

    fn __init__(
        inout self,
        stages: List[StageAnalysisItem],
        framework: EmergentFramework,
        example1: MojoCodeExample,
        util1: LowLevelUtilization,
        example2: MojoCodeExample,
        util2: LowLevelUtilization,
        conclusion: String
    ):
        self.stage_analysis = stages
        self.emergent_framework = framework
        self.mojo_code_example_1 = example1
        self.low_level_utilization_1 = util1
        self.mojo_code_example_2 = example2
        self.low_level_utilization_2 = util2
        self.conclusion = conclusion
