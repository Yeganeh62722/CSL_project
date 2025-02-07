section .text
global update_ball_position

; Function: update_ball_position
; Parameters:
;   RCX - pointer to ball_x (int)
;   RDX - pointer to ball_speed_x (int)
; Updates ball_x by adding the value in ball_speed_x
update_ball_position:
    ; Load ball_x value into RAX
    mov rax, [rcx]
    
    ; Load ball_speed_x value and add it to ball_x
    add rax, [rdx]
    
    ; Store the updated ball_x back
    mov [rcx], rax

    ret

