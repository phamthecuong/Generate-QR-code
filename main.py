import qrcode
import crcmod

def calculate_crc(data):
    crc16 = crcmod.predefined.mkPredefinedCrcFun('crc-ccitt-false')
    crc = hex(crc16(data.encode('utf-8'))).upper()[2:]
    return crc.zfill(4)

def get_str_length(payload):

    string = str(payload)

    account_no_lenght = len(string)
    if account_no_lenght < 10 :
        account_no_lenght = '0'+ str(account_no_lenght)

    return  account_no_lenght

def create_vietqr(bank_code, account_no, amount):
    # Dữ liệu đầu vào
    payload_format_indicator = "00" + "02" + "01"
    point_of_initiation_method = "01" + "02" + "11"

    bank_info = '00' + get_str_length(bank_code) + bank_code + '01' + get_str_length(account_no) + account_no

    account_info = '0010A00000072701' + str(len(bank_info)) + bank_info + '0208QRIBFTTA'

    consumer_account_information = '38' + str(len(account_info)) + account_info
    transaction_currency = "53" + "03" + "704"
    country_code = "58" + "02" + "VN"
    transaction_amount = "54" + get_str_length(amount) + str(amount)  # Ví dụ số tiền 19000 VND

    text_content = "Thanh toan hoa don"
    reference_label = "07" + str(len(text_content)) + text_content
    transfer_content = "62" + str(len(reference_label)) + reference_label

    # Tạo chuỗi dữ liệu
    data = (
        payload_format_indicator +
        point_of_initiation_method +
        consumer_account_information +
        transaction_currency +
        country_code +
        transaction_amount +
        transfer_content
    )

    # Tính CRC
    crc = calculate_crc(data + "6304")

    data += "63" + "04" + crc

    print(data)

    # Tạo mã QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save("vietqr_code.png")


vpbank_code = '970432'
account_no = '197993774'
amount = 10000

create_vietqr(vpbank_code, account_no, amount)