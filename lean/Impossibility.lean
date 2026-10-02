namespace CommunicationAbstraction

def runRounds {S H O : Type} (g : S → O → S) (a : H → O) : S → List H → S
  | s, [] => s
  | s, h :: hs => runRounds g a (g s (a h)) hs

theorem runRounds_congr {S H O : Type} (g : S → O → S) (a : H → O) :
    ∀ (s : S) (hs₁ hs₂ : List H), hs₁.map a = hs₂.map a →
      runRounds g a s hs₁ = runRounds g a s hs₂ := by
  intro s hs₁
  induction hs₁ generalizing s with
  | nil =>
    intro hs₂ h
    cases hs₂ with
    | nil => rfl
    | cons _ _ => simp at h
  | cons x xs ih =>
    intro hs₂ h
    cases hs₂ with
    | nil => simp at h
    | cons y ys =>
      simp only [List.map_cons, List.cons.injEq] at h
      simp only [runRounds]
      rw [h.1]
      exact ih _ ys h.2

structure BlindProtocol (S : Type) where
  init : Bool → S
  step : S → Nat → S
  decide : S → Bool
  rounds : Nat

def iter {S : Type} (f : S → S) : Nat → S → S
  | 0, x => x
  | k + 1, x => iter f k (f x)

def BlindProtocol.output {S : Type} (P : BlindProtocol S) (n : Nat) (x : Bool) : Bool :=
  P.decide (iter (fun s => P.step s n) P.rounds (P.init x))

def BlindProtocol.decision {S : Type} (P : BlindProtocol S) (n : Nat)
    (inputs : Nat → Bool) (i : Nat) : Bool :=
  P.output n (inputs i)

def Solves {S : Type} (P : BlindProtocol S) (n : Nat) : Prop :=
  (∀ inputs : Nat → Bool, ∀ v : Bool, (∀ i, i < n → inputs i = v) →
      ∀ i, i < n → P.decision n inputs i = v) ∧
  (∀ inputs : Nat → Bool, ∀ i j, i < n → j < n →
      P.decision n inputs i = P.decision n inputs j)

theorem blind_consensus_impossible {S : Type} (P : BlindProtocol S) (n : Nat)
    (hn : 2 ≤ n) : ¬ Solves P n := by
  intro ⟨hval, hagr⟩
  have h0 : 0 < n := by omega
  have h1 : 1 < n := by omega
  have ht : P.output n true = true :=
    hval (fun _ => true) true (fun _ _ => rfl) 0 h0
  have hf : P.output n false = false :=
    hval (fun _ => false) false (fun _ _ => rfl) 0 h0
  have hmix := hagr (fun i => if i = 0 then true else false) 0 1 h0 h1
  simp only [BlindProtocol.decision] at hmix
  simp at hmix
  rw [ht, hf] at hmix
  exact Bool.noConfusion hmix

def countObs {V : Type} [DecidableEq V] (msgs : List (Nat × V)) (v : V) : Nat :=
  (msgs.filter (fun m => decide (m.2 = v))).length

theorem countObs_rename {V : Type} [DecidableEq V] (σ : Nat → Nat) :
    ∀ (msgs : List (Nat × V)) (v : V),
      countObs (msgs.map (fun m => (σ m.1, m.2))) v = countObs msgs v := by
  intro msgs v
  induction msgs with
  | nil => rfl
  | cons m ms ih =>
    unfold countObs at *
    by_cases h : m.2 = v <;> simp [List.filter_cons, h, ih]

def kingValue {V : Type} : List (Nat × V) → Option V
  | [] => none
  | (s, v) :: ms => if s = 0 then some v else kingValue ms

theorem king_not_count_definable {V : Type} [DecidableEq V] (a b : V) (hab : a ≠ b) :
    ¬ ∃ g : (V → Nat) → Option V,
        ∀ msgs : List (Nat × V), g (countObs msgs) = kingValue msgs := by
  intro ⟨g, hg⟩
  let m₁ : List (Nat × V) := [(0, a), (1, b)]
  let m₂ : List (Nat × V) := [(1, a), (0, b)]
  have hc : countObs m₁ = countObs m₂ := by
    funext v
    unfold countObs
    by_cases ha : a = v <;> by_cases hb : b = v <;>
      simp [m₁, m₂, List.filter_cons, ha, hb]
  have h1 := hg m₁
  have h2 := hg m₂
  rw [hc, h2] at h1
  simp [kingValue, m₁, m₂] at h1
  exact hab h1.symm

end CommunicationAbstraction
