# H9 / H9_IMAGINE_PLANTED_BUBBLE_CLOSED_LOOP_V1
# CONTRACT PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1
# STAGE D3_TENSION_EXISTING_HANDLE — D3：沿既有側柄建立張力
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
["heroine_pose_tension", "shoulder_hip_weight_shift", "hair_and_cloth_followthrough"]

## MUST PRESERVE
["same_gripped_handle_track", "P", "base_contact", "cylinder_geometry", "outer_cap_clearance"]

## STAGE PROMPT
Starting from the accepted D2 image, increase the heroine's full-body tension and readable torque through the existing handle. This is one serial image edit, not a 20-cell pose board. The same hands grip the same pre-existing side rod; its attachment point, tangent axis, length, cylinder and planted conformal base remain locked. Do not swing/fly the cylinder toward the bubble: it is already planted. No premature cracks or shell damage.

## HARD OUTPUT RULES
- One serial full-frame photoreal image (16:9 preferred). NEVER a multi-cell control sheet.
- NO_NEW_HANDLE: outer circular end cap EMPTY; only the pre-existing side-middle lateral handle.
- Planted at P; cylinder axis = local bubble normal; glow only at conformal base seat.
- When person present: MINIATURE scale (full-body area ≈ hammer area); identity locked.
- D2 first grip: hands move to the existing side handle pixels — never invent a rod.
- E stages: cracks/shatter originate at the same P; shell only; sanctuary safe if present.
- code_visual_acceptance_status remains NOT_VERIFIED_BY_CODE until human pixel review.
