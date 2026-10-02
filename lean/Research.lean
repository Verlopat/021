namespace CommunicationAbstraction

structure FiniteMessage where
  label : String
  sender : Nat
  value : String
deriving DecidableEq, Repr

def l0 (m : FiniteMessage) : String := m.label
def l1 (m : FiniteMessage) : String × String := (m.label, m.value)
def l2 (m : FiniteMessage) : String × Nat × String := (m.label, m.sender, m.value)

theorem l0_factor_l1 (m : FiniteMessage) : l0 m = (l1 m).1 := by rfl

theorem l1_refines_l0 {m₁ m₂ : FiniteMessage} (h : l1 m₁ = l1 m₂) :
    l0 m₁ = l0 m₂ := congrArg Prod.fst h

def witnessA : FiniteMessage := { label := "proposal", sender := 0, value := "A" }
def witnessB : FiniteMessage := { label := "proposal", sender := 0, value := "B" }

theorem l0_collision_witness : l0 witnessA = l0 witnessB := by rfl

theorem l1_separates_witness : l1 witnessA ≠ l1 witnessB := by decide

end CommunicationAbstraction
