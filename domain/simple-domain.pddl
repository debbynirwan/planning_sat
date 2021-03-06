;; Specification in PDDL1 of the Simple domain

(define (domain simple)
 (:requirements :strips :typing)
 (:types
  location
  robot)

 (:predicates
   (adjacent ?l1  ?l2 - location)       ; location ?l1 is adjacent ot ?l2
   (atl ?r - robot ?l - location)       ; robot ?r is at location ?l
   )

;; moves a robot between two adjacent locations
 (:action move
     :parameters (?r - robot ?from ?to - location)
     :precondition (and (adjacent ?from ?to) (atl ?r ?from) )
     :effect (and (atl ?r ?to)
                    (not (atl ?r ?from)) )
 )
)
