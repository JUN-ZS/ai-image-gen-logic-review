# H9 / H9_IMAGINE_PLANTED_BUBBLE_CLOSED_LOOP_V1
# CONTRACT PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1
# STAGE D2_FIRST_GRIP_EXISTING_HANDLE — D2：首次握住來源圖已有的側柄
# provider=grok_imagine_serial_fullframe  (NO GEMINI_API_KEY required)

## Master
B3 geometry master file=B3_MASTER.jpg sha256=8ae5ecedcdc53d61efba59634ca1496d297a174598d30dbbedeba1f1be0953fe

## Person (when stage requires actor)
Heroine identity file=PERSON_REF.jpg sha256=f612ec7e07d95f256d3bd352f73f98ca913074c87556aed58cfc3223a059ee81

## GLOBAL LOCKS
- double-ended solid cylindrical hammer head, not a spherical mace or a T-v-T pair
- bubble-side conformal curved seat stays fully seated at P through every frame
- cylinder axis follows the local outward surface normal at P
- one existing handle attaches at the cylinder side-middle and runs tangent to the bubble
- handle instance/axis/length do not change after B; hands move to it at D2, not vice versa
- opposite outer circular end cap remains empty; no axial handle, lower stub, duplicate rod, or extra tool
- P, bubble center/radius, selected master geometry, camera/landmarks stay locked unless explicitly authorized
- base-interface glow and shell cracks originate from P; only the shell breaks; sanctuary/residents stay safe
- one serial full-frame image edit per step; never use a multi-cell image as evidence for per-frame locks

## AUTHORIZED DELTA ONLY
["heroine_hands_and_forearms", "minimum_required_arm_pose"]

## MUST PRESERVE
["P", "base_contact", "cylinder", "outer_cap_clearance", "existing_handle_pixels_and_axis"]

## STAGE PROMPT
Start from the accepted D1 parent and make only the first grip. Both hands must contact the exact already-existing side-middle handle identified by the supplied handle track/ROI. Move hands/forearms to the existing rod; never move the rod to the hands, grow a grip-friendly replacement, add a lower stub, or attach anything to either circular end cap. The rod keeps its same instance, attachment point, axis and length. Keep P and the conformal planted seat fixed; bubble remains intact and uncracked.

## HARD OUTPUT RULES
- One serial full-frame photoreal image (16:9 preferred). NEVER a multi-cell control sheet.
- NO_NEW_HANDLE: outer circular end cap EMPTY; only the pre-existing side-middle lateral handle.
- Planted at P; cylinder axis = local bubble normal; glow only at conformal base seat.
- When person present: MINIATURE scale (full-body area ≈ hammer area); identity locked.
- D2 first grip: hands move to the existing side handle pixels — never invent a rod.
- E stages: cracks/shatter originate at the same P; shell only; sanctuary safe if present.
- code_visual_acceptance_status remains NOT_VERIFIED_BY_CODE until human pixel review.
