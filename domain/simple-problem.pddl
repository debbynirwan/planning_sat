;; a simple problem
(define (problem simple-problem)
  (:domain simple)

  (:objects
   rob - robot
   loc1 loc2 - location)

  (:init
   (adjacent loc1 loc2)
   (adjacent loc2 loc1)
   (atl rob loc1)
   )

  (:goal
    (atl rob loc2)
   )
)
