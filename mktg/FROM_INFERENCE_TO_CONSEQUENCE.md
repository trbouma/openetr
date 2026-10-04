# From Inference to Consequence

### A human can create something. So can a machine. The harder question is what happens next.

I have been trying to find a simpler way to explain the problem I have been
working on with OpenETR.

The project began with electronic transferable records. Warehouse receipts.
Bills of lading. Records that do more than contain information because
something changes when they are issued, transferred, encumbered, discharged,
presented or terminated.

But the more I have worked on it, the less this has felt like a problem limited
to trade documents.

There is a more general architecture hiding underneath.

It has three parts:

**Inference.**

**Evidence.**

**Consequence.**

And I think keeping those three things separate may become increasingly
important as more of the digital world is created, interpreted and acted upon
by machines.

## Start With Something Created

Imagine that I sit down and write a document.

Perhaps it is a warehouse receipt. Perhaps it is a policy analysis, a poem, a
medical opinion or a permit. I have an idea, exercise some judgment and produce
something that did not exist before.

That is an act of inference in the broadest sense. I have interpreted the
world, brought experience and context to it, and produced an output.

Now imagine that an AI agent produces the document instead.

It reads a set of records, considers the surrounding circumstances, draws a
conclusion and generates the same output. Or perhaps the output is created
collaboratively. I provide the direction, the model develops the argument and
we revise it together until neither of us can say exactly where one
contribution ended and the other began.

From the perspective of the resulting digital artifact, does the distinction
matter?

It may matter a great deal for authorship, disclosure, accountability,
copyright, professional responsibility or institutional policy.

But it does not need to matter in order to identify the thing that was created.

The document has bytes. Those bytes can be given a cryptographic digest. The
digest identifies the exact digital artifact regardless of whether it came
from me, a machine, an organization, a sensor or some collaboration among
them.

That seems like a small observation.

I think it is actually quite important.

## Inference Is Not Only Something Machines Do

We have started using the word *inference* almost exclusively in connection
with AI.

Models perform inference. Agents infer intent. Systems infer classifications,
relationships and likely outcomes.

But people have always done this.

A doctor interprets symptoms. A warehouse operator examines goods. A customs
officer reviews a declaration. A judge evaluates evidence. An artist responds
to the world and creates something new. A person reading a document decides
what it means.

LLMs have not invented inference. They have made machine inference remarkably
general and inexpensive.

That changes a great deal. A machine can now read documents that were never
structured for it, compare unfamiliar vocabularies, summarize complex
histories and recommend what should happen next.

But inference still answers only one kind of question:

> What do we think?

It does not necessarily tell us what happened.

It certainly does not tell us what should have consequence.

## Then Comes Evidence

Suppose an AI agent reads a warehouse receipt and concludes that a particular
company controls it.

That may be a very good inference. The company may be named on the face of the
document. The agent may understand the relevant terminology. It may have seen
thousands of similar receipts.

But why should another party believe the conclusion?

Who issued the receipt? Is this the exact artifact that was issued? Was control
later transferred? Did the recipient accept it? Was the receipt pledged to a
lender? Was the pledge discharged? Was the record terminated?

The machine may be able to read the document perfectly and still have no
reliable way to answer those questions.

This is where evidence enters.

Evidence should let someone outside the originating application verify that a
particular actor made a particular statement concerning a particular thing.
The statement should be attributable. Its integrity should be testable. Its
relationship to earlier statements should be inspectable.

In the implementation I have been exploring, [Nostr](https://nips.nostr.com/1)
provides a remarkably small foundation for this. A signed event contains the
statement, the public key of the signer, a content-derived event identifier and
a signature. Events can refer to other events. Anyone with the event can
verify it.

Relays help distribute and retrieve the events. They are useful infrastructure,
but they are not the authority. The same event can exist on several relays, in
an application database, in an institutional archive or in a package exchanged
directly between two parties. Its identifier and signature remain the same.

That gives us a second question:

> What can we verify?

This is a much stronger question than *What does the application say?*

But it is still not enough.

## Evidence Does Not Decide What Follows

A valid signature proves that a key made a statement.

It does not prove that the statement was authorized. It does not prove that
the signer was a licensed warehouse operator, a government official, a doctor
or the rightful controller of a record. It does not prove that every relevant
event has been found.

Most importantly, it does not tell us what should change because the statement
exists.

Suppose I sign an event saying that I control your warehouse receipt. The event
may be perfectly valid. The signature may verify. The relay may store it. None
of that should make me the controller.

Something else is needed.

Rules.

The rules might say that only the current controller can initiate a transfer.
The intended recipient must accept it. An outstanding encumbrance may prevent
the transfer. A termination event may end the record's active lifecycle. A
particular institution may require an additional attestation before it
recognizes any of this.

Once we evaluate the evidence under those rules, we can determine what follows.

That is what I mean by **Consequence**.

And it gives us the third question:

> What follows from this evidence under these rules?

## The Artifact May Become Consequential

Not every digital artifact needs consequential state.

This essay probably does not.

You can read it, share it, disagree with it or forget it. Its meaning may
matter, but there is no particular reason that it needs a control lifecycle.

The situation changes if the artifact becomes the subject of something that
must be independently established.

Perhaps it is formally published and later corrected. Perhaps a licence is
issued for its use. Perhaps it becomes evidence of an institutional decision.
Perhaps an agreement gives it contractual significance. Perhaps the artifact
is a receipt whose control determines who can demand delivery of goods.

The content has not become more digital.

It has become consequential.

This is the distinction at the heart of
[OpenETR](https://docs.openetr.org).

A **Digital Artifact** is persistent content identified by a digest.

A **Digital Controllable Record** is the signed evidence concerning that
artifact.

**Consequential State** is what follows when that evidence is validated and
evaluated according to identified rules.

The artifact plus its established Consequential State becomes what OpenETR
calls a **Digital Original**.

That is a different way to think about originality. It is not based on the
impossibility of copying bytes. Digital things are copied constantly. It is
based on the ability to establish what has happened concerning the thing and
what state follows.

A copy can reproduce content.

It cannot independently reproduce consequence.

## Human and Machine Creation Can Enter the Same Architecture

This brings me back to the question of who created the artifact.

At the protocol layer, OpenETR does not need to know whether the original
inference came from a human or a machine.

It begins with the resulting artifact.

What is it? Which exact content are we talking about? What signed evidence
concerns it? Which rules apply? What state follows?

That gives human and machine creative acts something like equal technical
standing. Both can produce artifacts. Both can make signed statements. Both
can participate in an evidence graph. Both can be evaluated under rules.

This does not mean every institution has to treat them identically.

A court may require a human declaration. A medical system may require a
licensed professional to approve an AI-generated opinion. A government may
require disclosure that an artifact was machine-generated. A company may
permit an agent to act only within a narrow mandate. Copyright law may care
deeply about human authorship.

Fine.

Those are recognition rules.

The important point is that they do not need to be hidden inside the basic
identity of the artifact. The artifact can be identified first. Evidence can
be evaluated. Then the recognizing party can apply whatever distinctions the
context requires.

Origin may explain how the artifact came to exist.

Evidence and rules determine whether it has consequential state.

Recognition determines what standing and effect that state receives.

## The Application Should Not Own the Answer

Most digital systems do not separate these layers.

The application interprets the input. The application records what happened.
The application updates a database. The application decides what the user may
do next. The application displays the resulting state.

As long as everyone trusts the application and it continues running, this can
work perfectly well.

But if the application disappears, changes vendors, withdraws access, loses
its database or simply stops cooperating, where did the consequence go?

That is the architectural problem that continues to interest me.

An application should be able to provide an excellent interface. It should
authenticate users, enforce permissions, protect keys, guide workflows,
display state and help people understand what is happening.

It just should not have to be the only place from which the answer can be
known.

If another authorized party has the artifact, the signed evidence and the
identified rules, it should be capable of arriving at the same technical
result independently.

The application becomes an interface rather than the ultimate authority.

## One Architecture, Particular Technologies

This leaves me with a formulation I rather like:

> **Inference interprets.**
>
> **Evidence establishes what can be verified.**
>
> **Consequence determines what follows under identified rules.**

This is a general architecture. It does not depend on any one technology.

People, statistical models and rules engines can all perform inference.
Evidence can be preserved through signatures, archives, registries,
content-addressed storage or other protocols. Consequence can be determined by
institutional rule books, statutory rules, registries, smart contracts or
deterministic protocol validators.

The implementation I am working with happens to look like this:

> **LLMs provide a powerful implementation of inference.**
>
> **Signed Nostr events provide a portable implementation of evidence.**
>
> **OpenETR provides an implementation of consequence.**

LLMs can interpret an artifact and help us reason about it. Nostr can carry
signed evidence concerning it. OpenETR can organize that evidence into a
Digital Controllable Record and determine its Consequential State under an
identified rule book.

Then recognition begins.

A bank, court, warehouse, regulator, community, merchant or individual decides
whether it accepts the actors, evidence, rules and resulting state for the
purpose at hand.

That final step should not be treated as an inconvenient detail.

It is where authority belongs.

## A Larger Ecosystem

I started with transferable records because the consequence is easy to see.

A warehouse receipt is not important only because of what it says. It matters
because control of the receipt can affect control of goods. A bill of lading
can be transferred, presented and surrendered. An encumbrance can affect what
another party is permitted to do.

But the same architecture appears elsewhere.

A health record may be issued, corrected, superseded or withdrawn.

An academic record may be awarded and later amended or revoked.

A product record may be inspected, repaired, recalled or retired.

An authorization given to an AI agent may be active, exercised, expired or
revoked.

In each case, interpretation matters. Evidence matters. Consequence matters.
And recognition remains contextual.

This suggests a larger digital ecosystem in which creative acts by people and
machines can enter through the same front door.

Some will remain content.

Some will become evidence.

Some will acquire Consequential State.

The architecture does not need to decide in advance which is which.

It needs to make the transition independently verifiable when something does
follow.

## What Comes Next

AI is making digital artifacts much easier to create and interpret.

That is extraordinary. It may also tempt us to collapse interpretation,
evidence and authority into the same system. The model reads the document,
decides what it means, takes an action and updates the database. The interface
shows the new state. Everything feels complete.

Until someone outside the system asks why the state is true.

At that point, we need more than an inference.

We need evidence another party can verify.

We need rules that make clear what follows.

And we need recognizing parties willing and entitled to decide what effect the
result should have.

Maybe a person created the artifact.

Maybe a machine did.

Maybe they created it together.

First, identify the thing.

Then preserve the evidence.

Then determine what follows.

Recognition gives it effect.

That, I think, is the architecture.
