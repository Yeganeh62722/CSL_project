section .text
    global update_ball_position

; Function: update_ball_position
; Parameters:
;   RCX - pointer to ball_x (int)
;   RDX - pointer to ball_speed_x (int)
; Updates ball_x by adding the value in ball_speed_x
update_ball_position:

    ; Load ball_x and ball_speed_x
    movss xmm0, [rcx]         ; xmm0 = ball_x
    movss xmm1, [rdx]         ; xmm1 = ball_speed_x
    addps xmm0, xmm1          ; ball_x += ball_speed_x
    movss [rcx], xmm0         ; Store updated ball_x

    ret

