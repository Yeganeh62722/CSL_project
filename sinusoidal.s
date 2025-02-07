section .text
    global update_sinusoidal_ball_position

; Function: update_sinusoidal_ball_position
; Parameters:
;   RCX - pointer to ball_x (float)
;   RDX - pointer to ball_y (float)
;   R8  - pointer to ball_speed_x (float)
;   R9  - pointer to sinusoidal_angle (float)

update_sinusoidal_ball_position:
    ; Load ball_x and ball_speed_x
    movss xmm0, [rcx]         ; xmm0 = ball_x
    movss xmm1, [r8]          ; xmm1 = ball_speed_x
    addss xmm0, xmm1          ; ball_x += ball_speed_x
    movss [rcx], xmm0         ; Store updated ball_x

    ; Increment sinusoidal angle
    mov dword [rel sin_increment_val], 0x3DCCCCCD ; 0.1 as 32-bit float
    movss xmm2, [rel sin_increment_val]
    movss xmm3, [r9]          ; xmm3 = sinusoidal_angle
    addss xmm3, xmm2          ; sinusoidal_angle += 0.1
    movss [r9], xmm3          ; Store updated sinusoidal_angle

    ; Compute ball_y using the formula: ball_y = 700 - 50 * sin(sinusoidal_angle)
    fld dword [r9]            ; Load sinusoidal_angle onto the FPU stack
    fsin                      ; Compute sin(sinusoidal_angle)
    fmul dword [rel sin_amplitude_val] ; Multiply by 50.0
    fld dword [rel base_height] ; Load 700.0
    fsub                      ; 700 - result
    fstp dword [rdx]          ; Store updated ball_y

    ret

section .data
    sin_increment_val dd 0.0          ; Constant for sinusoidal increment (0.1)
    sin_amplitude_val dd 50.0         ; Amplitude for sinusoidal function
    base_height dd 700.0              ; Base height value
