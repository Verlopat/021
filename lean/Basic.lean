namespace CommunicationAbstraction

/-- Abstract L0 observation function. The concrete Python implementation uses
    canonical label counts; the theorem captures the semantic factorization
    requirement independently of representation details. -/
def FactorsThrough {State History Obs : Type} (a : History → Obs) (t : State → History → State) : Prop :=
  ∃ g : State → Obs → State, ∀ s h, t s h = g s (a h)

/-- An L0 transition cannot distinguish histories with the same observation. -/
theorem l0_factorization_invariant
    {State History Obs : Type}
    {a : History → Obs}
    {t : State → History → State}
    (hfactor : FactorsThrough a t)
    {s : State} {h₁ h₂ : History}
    (heq : a h₁ = a h₂) :
    t s h₁ = t s h₂ := by
  rcases hfactor with ⟨g, hg⟩
  simp [hg, heq]

/-- The induced indistinguishability relation is an equivalence relation. -/
def Indistinguishable {History Obs : Type} (a : History → Obs) (h₁ h₂ : History) : Prop :=
  a h₁ = a h₂

theorem indistinguishable_refl
    {History Obs : Type} (a : History → Obs) (h : History) :
    Indistinguishable a h h := by
  rfl

theorem indistinguishable_symm
    {History Obs : Type} (a : History → Obs) {h₁ h₂ : History} :
    Indistinguishable a h₁ h₂ → Indistinguishable a h₂ h₁ := by
  intro h
  exact h.symm

theorem indistinguishable_trans
    {History Obs : Type} (a : History → Obs) {h₁ h₂ h₃ : History} :
    Indistinguishable a h₁ h₂ → Indistinguishable a h₂ h₃ → Indistinguishable a h₁ h₃ := by
  intro h12 h23
  exact h12.trans h23

end CommunicationAbstraction
