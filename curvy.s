section .text
    global update_curve_ball_position

; Function: update_curve_ball_position
; Parameters:
;   RCX - pointer to ball_x (float)
;   RDX - pointer to ball_y (float)
;   R8  - pointer to ball_speed_x (float)
;   R9  - pointer to ball_speed_y (float)

update_curve_ball_position:
    ; Load ball_x and ball_speed_x
    movss xmm0, [rcx]         ; xmm0 = ball_x
    movss xmm1, [r8]          ; xmm1 = ball_speed_x
    addss xmm0, xmm1          ; ball_x += ball_speed_x
    movss [rcx], xmm0         ; Store updated ball_x

    ; Load ball_y and ball_speed_y
    movss xmm2, [rdx]         ; xmm2 = ball_y
    movss xmm3, [r9]          ; xmm3 = ball_speed_y
    addss xmm2, xmm3          ; ball_y += ball_speed_y
    movss [rdx], xmm2         ; Store updated ball_y

    ; Update ball_speed_y by adding 0.07
    mov dword [rel gravity_val], 0x3DCCCCCD  ; 0.07 as 32-bit float
    movss xmm4, [rel gravity_val]
    addss xmm3, xmm4          ; ball_speed_y += 0.07
    movss [r9], xmm3          ; Store updated ball_speed_y

    ret

section .data
    gravity_val dd 0.0        ; Constant for gravity (0.07)
