from singleton.singleton import s

if __name__ == "__main__":
    s1 = s
    s2 = s
    print(s1 is s2)
    print(s1 == s2)
    print(id(s1) == id(s2))
