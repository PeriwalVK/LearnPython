A = [42, 7, 19, 73, 3, 58, 91, 24, 16, 65, 7, 19, 42, 3, 53]
B = []


# we will keep it aside and then
while A:
    # Keep putting elements in B ensuring B always have non-increasing elements
    while A and B and A[-1] <= B[-1]:
        B.append(A.pop())

    if A:
        # kept_aside: first such element which is going to break non-increasing nature of B
        kept_aside = A.pop()

        # keep popping from B to A until we find right place for kept_aside in B
        while B and B[-1] < kept_aside:
            A.append(B.pop())

        # put kept_aside in B
        B.append(kept_aside)

# Now put back all elts from B back to A to reach final state
while B:
    A.append(B.pop())

print(A)
