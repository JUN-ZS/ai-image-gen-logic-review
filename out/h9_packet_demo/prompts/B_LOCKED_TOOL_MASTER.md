# H9 / H9_IMAGINE_PLANTED_BUBBLE_CLOSED_LOOP_V1
# CONTRACT PLANTED_DOUBLE_ENDED_CYLINDER_BUBBLE_CONTACT_V1
# STAGE B_LOCKED_TOOL_MASTER — B：隔離並鎖定單一種植圓柱母版
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
["isolate_selected_tool_roi", "remove_other_candidate_tools"]

## MUST PRESERVE
["bubble_center_radius", "P", "conformal_base_seat", "cylinder_axis", "outer_cap", "side_middle_handle"]

## STAGE PROMPT
Make one isolated master from the exact selected ROI in the source atlas. Keep exactly one double-ended cylindrical hammer head planted on the bubble surface. The bubble-side end has a conformal curved seat fully contacting the bubble at P and a restrained glow at that base interface. The cylinder axis follows the local outward surface normal. One existing straight handle attaches at the cylinder side-middle and extends along the local tangent (transverse to the cylinder axis, about 90 degrees). Keep the opposite outer circular end cap completely clear: no rod or handle extends axially from it. Do not redraw the tool, change its proportions, move P, or create a flying hammer. No person, no cracks, no broken shell. This is one full-frame image, not a grid.

## HARD OUTPUT RULES
- One serial full-frame photoreal image (16:9 preferred). NEVER a multi-cell control sheet.
- NO_NEW_HANDLE: outer circular end cap EMPTY; only the pre-existing side-middle lateral handle.
- Planted at P; cylinder axis = local bubble normal; glow only at conformal base seat.
- When person present: MINIATURE scale (full-body area ≈ hammer area); identity locked.
- D2 first grip: hands move to the existing side handle pixels — never invent a rod.
- E stages: cracks/shatter originate at the same P; shell only; sanctuary safe if present.
- code_visual_acceptance_status remains NOT_VERIFIED_BY_CODE until human pixel review.
