# Scope Analysis Patterns

Reference guide for classifying client requests against a SOW or contract.

## Classification Patterns

### IN SCOPE - clear signals
- The request names a deliverable that appears verbatim or near-verbatim in the SOW
- The request is a natural sub-task of a named deliverable (e.g. "fix a bug" when SOW includes "bug fixes during UAT period")
- The SOW includes a broad category that clearly encompasses the request (e.g. "ongoing support" covering a configuration question)
- The request is within the stated timeline and has not been previously flagged as additional work

### OUT OF SCOPE - clear signals
- The request names something explicitly listed in the "Out of Scope" section
- The request is a new deliverable not mentioned anywhere in the SOW
- The SOW states a fixed number of items (e.g. "3 design revisions") and this would exceed that
- The request relates to a system, platform, or workstream not mentioned in the SOW
- The request was previously discussed and deferred or declined during the engagement

### GREY AREA - common sources of ambiguity
- The SOW uses vague language ("reasonable support", "standard delivery", "as required")
- The request is a logical extension of a deliverable but goes beyond what was explicitly described
- The timeline has ended but the deliverable was not fully signed off
- The SOW covers a category (e.g. "training") but does not define the volume or format
- The client is asking for something that was mentioned informally in emails but not written into the SOW

## Edge Cases

### Maintenance vs. new development
If the SOW includes a "maintenance" or "support" phase, distinguish between:
- **Maintenance** = keeping the agreed deliverable working as specified (IN SCOPE)
- **Enhancement** = adding new capability or changing behaviour beyond the original spec (OUT OF SCOPE or change request)

### Defect vs. change request
- A defect is something that does not work as the SOW specifies it should → IN SCOPE to fix
- A change is something the client now wants to work differently → OUT OF SCOPE, triggers change control

### Verbal agreements
If the user mentions something was "agreed verbally" or "discussed in a call" but is not in the SOW, classify it as GREY AREA and note that verbal agreements are not enforceable under the SOW's change control clause.

### Rush or urgency
Urgency does not change scope. A request being urgent does not make it in scope. Note this clearly if relevant.

## Draft Response Tone Guide

| Verdict | Tone | Key message |
|---|---|---|
| IN SCOPE | Confirmatory | Confirm it's covered, set expectations on timeline |
| Out of Scope | Firm but collaborative | Acknowledge the need, explain it's outside the current agreement, offer change control path |
| Grey Area | Transparent | Name the ambiguity, propose how to resolve it (change request or joint interpretation) |

## Change Control Language

If a change request is needed, the draft response should:
1. Acknowledge the client's request positively
2. State clearly it falls outside the current SOW
3. Offer to assess and quote via the change control process
4. Not begin any work until sign-off

Example: "This falls outside the scope of our current agreement. I am happy to assess what would be involved and provide a change request for your approval before we proceed."
