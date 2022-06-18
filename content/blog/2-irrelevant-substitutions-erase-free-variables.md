+++
title = "Irrelevant Substitutions Erase Free Variables"
date = 2022-06-14
draft = true

[taxonomies]
categories = ["Musings"]
tags = ["cedille", "research"]

[extra]
lang = "en"
toc = true
show_comment = false
math = true
mermaid = false
+++


```ced
Cast : ★ ➔ ★ ➔ ★
= λ A B. ι f: A ➔ B. {f ≃ λ x. x}.

intrCast : ∀ A:★. ∀ B:★. ∀ f:A ➔ B.
    (Π a:A. {f a ≃ a}) ➾ Cast·A·B
= λ -A -B -f -eq. [λ a. φ (eq a) - (f a) {a}, β].

cast : ∀ A:★. ∀ B:★. Cast·A·B ➾ A ➔ B
= λ -A -B -c. φ c.2 - c.1 {λ x. x}.
```


```ced
irrelEq : ∀ A:★. ∀ B:★. ∀ t:A. ∀ s:B. {t ≃ s} ➾ {t ≃ s}
= λ -t -s -eq. ρ eq - β.
```

```ced
Top : ★ = {β ≃ β}

omega : Top
```