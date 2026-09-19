Source: https://docs.typesafe.ai/sdk/python/api/types/responses
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Answers and responses

> Read answers, confidence scores, token usage, and available models returned by the TypeSafe API.

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




  Response



  typesafe\_sdk.SystemOneResponse


Bases: `Response`

Answers grouped by question type with model and usage metadata.

See [System One](../../../../concepts/system-one.md) for details.


  request\_id


`cached` `property`

<SdkSignature>
  
    request_id
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>

The `x-typesafe-request-id` response header.


  raw\_http\_response


`property`

```python theme={null}
raw_http_response: httpx2.Response
```

The underlying `httpx2.Response`, exposing status, headers, and body.


  model


`instance-attribute`

<SdkSignature>
  
    model
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>

The model used to answer the request.


  usage


`instance-attribute`

<SdkSignature>
  
    usage
  

  
    :
  

   

  
    
      Usage
    
  

  

</SdkSignature>

Token usage for the request.


  answers


`class-attribute` `instance-attribute`

<SdkSignature>
  answers: dict[str, Answer] = field(
    default_factory=dict
)

</SdkSignature>

All answer objects keyed by question name.


  nouls


`cached` `property`

<SdkSignature>
  
    nouls
  

  
    :
  

   

  
    
      dict
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      NoulAnswer
    
  

  
    ]
  

  

</SdkSignature>

Yes/no answers keyed by question name.


  choices


`cached` `property`

<SdkSignature>
  
    choices
  

  
    :
  

   

  
    
      dict
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      ChoiceAnswer
    
  

  
    ]
  

  

</SdkSignature>

Choice answers keyed by question name.


  scores


`cached` `property`

<SdkSignature>
  
    scores
  

  
    :
  

   

  
    
      dict
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      ScoreAnswer
    
  

  
    ]
  

  

</SdkSignature>

Score answers keyed by question name.


  typesafe\_sdk.Usage


Bases: <code>msgspec.Struct</code>

Token counts for a request, when reported by the API.


  input\_tokens


`class-attribute` `instance-attribute`

<SdkSignature>
  
    input_tokens
  

  
    :
  

   

  
    
      int
    
  

   

  
    |
  

   

  
    None
  

   

  
    =
  

   

  
    None
  

  

</SdkSignature>

Number of input tokens used, or `None` when the API did not report it.


  output\_tokens


`class-attribute` `instance-attribute`

<SdkSignature>
  
    output_tokens
  

  
    :
  

   

  
    
      int
    
  

   

  
    |
  

   

  
    None
  

   

  
    =
  

   

  
    None
  

  

</SdkSignature>

Number of output tokens used, or `None` when the API did not report it.


  Answers



  typesafe\_sdk.NoulAnswer


Bases: `wire.NoulAnswer`

A yes/no answer.

See the [noul primitive](../../../../primitives/noul.md) for details.


  noul


`instance-attribute`

<SdkSignature>
  
    noul
  

  
    :
  

   

  
    
      float
    
  

  

</SdkSignature>

Probability of a yes answer, from zero to one.


  typesafe\_sdk.ChoiceAnswer


Bases: `wire.ChoiceAnswer`

A selected label and its probabilities.

See the [choice primitive](../../../../primitives/choice.md) for details.


  choice


`instance-attribute`

<SdkSignature>
  
    choice
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>

The selected label.


  confidence


`instance-attribute`

<SdkSignature>
  
    confidence
  

  
    :
  

   

  
    
      float
    
  

  

</SdkSignature>

Reported confidence in the selected label.


  probabilities


`instance-attribute`

<SdkSignature>
  
    probabilities
  

  
    :
  

   

  
    
      dict
    
  

  
    [
  

  
    
      str
    
  

  
    ,
  

   

  
    
      float
    
  

  
    ]
  

  

</SdkSignature>

Probabilities keyed by label.


  typesafe\_sdk.ScoreAnswer


Bases: `wire.ScoreAnswer`

An expected score with its rubric and probabilities.

See the [score primitive](../../../../primitives/score.md) for details.


  score


`instance-attribute`

<SdkSignature>
  
    score
  

  
    :
  

   

  
    
      float
    
  

  

</SdkSignature>

Expected score, which may fall between the integer rubric levels.


  confidence


`instance-attribute`

<SdkSignature>
  
    confidence
  

  
    :
  

   

  
    
      float
    
  

  

</SdkSignature>

Reported confidence in the score.


  legend


`instance-attribute`

<SdkSignature>
  legend: dict[
    int, str | dict[str, Any] | list[Any]
]

</SdkSignature>

Rubric descriptions keyed by integer score.


  probabilities


`instance-attribute`

<SdkSignature>
  
    probabilities
  

  
    :
  

   

  
    
      dict
    
  

  
    [
  

  
    
      int
    
  

  
    ,
  

   

  
    
      float
    
  

  
    ]
  

  

</SdkSignature>

Probabilities keyed by integer score.


  typesafe\_sdk.Answer


`module-attribute`

<SdkSignature>
  Answer: TypeAlias = (
    NoulAnswer | ChoiceAnswer | ScoreAnswer
)

</SdkSignature>

An answer to a single question, identified by its `type`.


  Available models



  typesafe\_sdk.ListModelsResponse


Bases: `Response`

The models available to the account.


  request\_id


`cached` `property`

<SdkSignature>
  
    request_id
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>

The `x-typesafe-request-id` response header.


  raw\_http\_response


`property`

```python theme={null}
raw_http_response: httpx2.Response
```

The underlying `httpx2.Response`, exposing status, headers, and body.


  models


`instance-attribute`

<SdkSignature>
  
    models
  

  
    :
  

   

  
    
      tuple
    
  

  
    [
  

  
    
      ModelMetadata
    
  

  
    ,
  

   

  
    ...
  

  
    ]
  

  

</SdkSignature>

The available models.


  typesafe\_sdk.ModelMetadata


Bases: <code>Struct</code>


  name


`instance-attribute`

<SdkSignature>
  
    name
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>


  description


`instance-attribute`

<SdkSignature>
  
    description
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>


  release\_date


`instance-attribute`

<SdkSignature>
  
    release_date
  

  
    :
  

   

  
    
      str
    
  

  

</SdkSignature>
