from upload import Upload

test = Upload("Test.pdf")
test.sid = "lbu1bomd9og3epzf"
test.fid = "o_1ap1na2u8v4u16mu5bose218gd1"
test.convert_result = "Test.doc"
print("Starting download")
print(test.download("Test.doc"))
