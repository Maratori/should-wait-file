from file import File

if __name__ == '__main__':
    file = File("aaa")
    print(file.should)
    print(file.should.exist)
    print(file.should.Not)
    print(file.should.Not.Not)
    print(file.should.Not.Not.Not)
    print(file.should.Not.exist)

    file.should.exist()
    file.should.Not.Not.exist()
    # file.should.Not.exist()

    file.should.have.size.eq()
