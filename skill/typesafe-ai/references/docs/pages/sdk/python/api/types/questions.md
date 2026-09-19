Source: https://docs.typesafe.ai/sdk/python/api/types/questions
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Questions

> Provide state and ask yes/no, choice, and score questions using objects or dictionaries.

export function SdkSignature({children}) {
  async function copy(event) {
    const button = event.currentTarget;
    const code = button.parentElement.querySelector("pre code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.setAttribute("aria-label", "Signature copied");
      button.dataset.copied = "true";
    } catch {
      button.setAttribute("aria-label", "Copy failed; select the signature to copy");
    }
    setTimeout(() => {
      button.setAttribute("aria-label", "Copy signature");
      delete button.dataset.copied;
    }, 2000);
  }
  return 
      <button type="button" className="sdk-signature-copy" aria-label="Copy signature" onClick={copy}>
        <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <rect x="8" y="8" width="12" height="12" rx="2" />
          <path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3" />
        </svg>
      </button>
      <pre tabIndex={0} aria-label="SDK signature"><code>{children}</code></pre>
    ;
}




  State


`state` is the text or JSON object you want to ask questions about. It cannot be `None`, but values inside an object may be `None`.


  Question objects


Use `Noul`, `Choice`, and `Score` to define questions with named arguments.


  typesafe\_sdk.NoulCriteria


Bases: <code>TypedDict</code>

Optional descriptions of the yes and no outcomes.

See the [noul primitive](../../../../primitives/noul.md) for details.


  true


`instance-attribute`

<SdkSignature>
  
    true
  

  
    :
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  

</SdkSignature>

Description of the yes outcome as text, a JSON object, or an array; `None` leaves it undescribed.


  false


`instance-attribute`

<SdkSignature>
  
    false
  

  
    :
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  

</SdkSignature>

Description of the no outcome as text, a JSON object, or an array; `None` leaves it undescribed.


  typesafe\_sdk.Noul


Bases: `wire.NoulQuestion`

A yes/no question with optional descriptions for either outcome.

See the [noul primitive](../../../../primitives/noul.md) for details.


  instructions


`class-attribute` `instance-attribute`

<SdkSignature>
  
    instructions
  

  
    :
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

   

  
    =
  

   

  
    None
  

  

</SdkSignature>

The question to ask, expressed as text, a JSON object, or an array; optional.


  criteria


`class-attribute` `instance-attribute`

<SdkSignature>
  
    criteria
  

  
    :
  

   

  
    
      NoulCriteria
    
  

   

  
    |
  

   

  
    None
  

   

  
    =
  

   

  
    None
  

  

</SdkSignature>

Optional descriptions of the yes and no outcomes.


  typesafe\_sdk.Choice


Bases: `wire.ChoiceQuestion`

A question that selects between named alternatives.

See the [choice primitive](../../../../primitives/choice.md) for details.


  criteria


`instance-attribute`

<SdkSignature>
  
    criteria
  

  
    :
  

   

  
    
      Mapping
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  
    ]
  

  

</SdkSignature>

Labels mapped to text, object, or array descriptions, or `None` for undescribed labels.


  instructions


`class-attribute` `instance-attribute`

<SdkSignature>
  
    instructions
  

  
    :
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

   

  
    =
  

   

  
    None
  

  

</SdkSignature>

The question to ask, expressed as text, a JSON object, or an array; optional.


  typesafe\_sdk.Score


Bases: `wire.ScoreQuestion`

A question that assigns a score using an ordered rubric.

See the [score primitive](../../../../primitives/score.md) for details.


  criteria


`instance-attribute`

<SdkSignature>
  
    criteria
  

  
    :
  

   

  
    
      Sequence
    
  

  
    [
  

  
    
      JSONContent
    
  

  
    ]
  

  

</SdkSignature>

A nonempty, ordered list of text, object, or array descriptions, one per score from zero.


  instructions


`class-attribute` `instance-attribute`

<SdkSignature>
  
    instructions
  

  
    :
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

   

  
    =
  

   

  
    None
  

  

</SdkSignature>

The question to ask, expressed as text, a JSON object, or an array; optional.


  typesafe\_sdk.Question


`module-attribute`

<SdkSignature>
  Question: TypeAlias = (
    Noul | Choice | Score | QuestionModel
)

</SdkSignature>

A question object or question dictionary.


  typesafe\_sdk.Questions


`module-attribute`

<SdkSignature>
  
    Questions
  

  
    :
  

   

  
    
      TypeAlias
    
  

   

  
    =
  

   

  
    
      Mapping
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      Question
    
  

  
    ]
  

  

</SdkSignature>

Question inputs keyed by the names used to identify their answers.


  Question dictionaries


Question dictionaries include a `type` key: `"noul"`, `"choice"`, or `"score"`. You can mix dictionaries and question objects in the same request.


  typesafe\_sdk.NoulModel


Bases: <code>TypedDict</code>

A yes/no question dictionary with `type="noul"`, allowing extra JSON fields.

See the [noul primitive](../../../../primitives/noul.md) for details.


  type


`instance-attribute`

<SdkSignature>
  
    type
  

  
    :
  

   

  
    
      Literal
    
  

  
    [
  

  
    'noul'
  

  
    ]
  

  

</SdkSignature>


  instructions


`instance-attribute`

<SdkSignature>
  
    instructions
  

  
    :
  

   

  
    
      NotRequired
    
  

  
    [
  

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  
    ]
  

  

</SdkSignature>

The question to ask, expressed as text, a JSON object, or an array; optional.


  criteria


`instance-attribute`

<SdkSignature>
  
    criteria
  

  
    :
  

   

  
    
      NotRequired
    
  

  
    [
  

  
    
      NoulCriteria
    
  

   

  
    |
  

   

  
    None
  

  
    ]
  

  

</SdkSignature>

Optional descriptions of the yes and no outcomes.


  typesafe\_sdk.ChoiceModel


Bases: <code>TypedDict</code>

A choice question dictionary with `type="choice"`, allowing extra JSON fields.

See the [choice primitive](../../../../primitives/choice.md) for details.


  type


`instance-attribute`

<SdkSignature>
  
    type
  

  
    :
  

   

  
    
      Literal
    
  

  
    [
  

  
    'choice'
  

  
    ]
  

  

</SdkSignature>


  instructions


`instance-attribute`

<SdkSignature>
  
    instructions
  

  
    :
  

   

  
    
      NotRequired
    
  

  
    [
  

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  
    ]
  

  

</SdkSignature>

The question to ask, expressed as text, a JSON object, or an array; optional.


  criteria


`instance-attribute`

<SdkSignature>
  
    criteria
  

  
    :
  

   

  
    
      Mapping
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  
    ]
  

  

</SdkSignature>

Labels mapped to text, object, or array descriptions, or `None` for undescribed labels.


  typesafe\_sdk.ScoreModel


Bases: <code>TypedDict</code>

A score question dictionary with `type="score"`, allowing extra JSON fields.

See the [score primitive](../../../../primitives/score.md) for details.


  type


`instance-attribute`

<SdkSignature>
  
    type
  

  
    :
  

   

  
    
      Literal
    
  

  
    [
  

  
    'score'
  

  
    ]
  

  

</SdkSignature>


  instructions


`instance-attribute`

<SdkSignature>
  
    instructions
  

  
    :
  

   

  
    
      NotRequired
    
  

  
    [
  

  
    
      JSONContent
    
  

   

  
    |
  

   

  
    None
  

  
    ]
  

  

</SdkSignature>

The question to ask, expressed as text, a JSON object, or an array; optional.


  criteria


`instance-attribute`

<SdkSignature>
  
    criteria
  

  
    :
  

   

  
    
      Sequence
    
  

  
    [
  

  
    
      JSONContent
    
  

  
    ]
  

  

</SdkSignature>

A nonempty, ordered list of text, object, or array descriptions, one per score from zero.


  typesafe\_sdk.QuestionModel


`module-attribute`

<SdkSignature>
  QuestionModel: TypeAlias = (
    NoulModel | ChoiceModel | ScoreModel
)

</SdkSignature>

A question dictionary identified by its `type` key.
