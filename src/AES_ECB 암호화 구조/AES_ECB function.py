
# AES128_ECB 암호화 구조

def AES128_ECB(plain_block, whole_key, round=10):
  
  # plain_block 위치에 4*4 리스트 넣기
  # 한 블럭당 16byte
  
    cipher_block = copy.deepcopy(plain_block) # import copy -> copy 모듈을 이용한 deepcopy함수 사용 : deepcopy는 깊은 복사로 내부 객체들까지 모두 새롭게 copy되는 함수이다.

    for i in range(4):
      
        for j in range(4):
          
            cipher_block[i][j] ^= whole_key[0][i][j]
  
    for i in range(1,round+1):
      
        cipher_block = SubBytes(cipher_block) # SubByte 함수는 Plain Text 값을 S-Box의 값으로 치환하는 함수이다. 
        cipher_block = ShiftRows(cipher_block) # ShiftRows 함수는 S-Box이후 만들어진 값을 규칙대로 옮겨주는 함수이다. (ShiftRow 함수는 행을 왼쪽으로 순환 시프트 시켜주는 함수를 의미한다.)

        if i != round:
          
            cipher_block = MixColumns(cipher_block) # Mixcolumns 함수는 ShiftRow 함수에서 정렬한 행렬과 각각의 열(Column)들을 곱해주는 연산을 해줍니다.
    
        for j in range(4):
        
            for k in range(4):
            
                cipher_block[j][k] ^= whole_key[i][j][k] 

    return cipher_block  
  
