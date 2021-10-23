guests = ["Alice", "Bob", "Carol", "David" ]
invites = [1] * 3 + [0]
def is_invited(guest, inv, no):
    if inv:
        print(f"Guest {no}: Welcome, {guest}")
    else:
        print(f"Guest {no}: You are not invited, {guest}")
for no, (guest, inv) in enumerate(zip(guests, invites)):
    is_invited(guest, inv, no)
