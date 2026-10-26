**Task: "You just arrived. Get in line for [one of your services]."**

- Did they finish it?
   Yes!
-About how long it took? 
   About 6 seconds
-Where they hesitated, what they said, and anything that surprised you.
   The user did not hesitate and said nothing.


-Which of your persona's "Because …, my interface must …" rules held up, and which did not
   "Because he is already old and have eye condition, I generally need to make the fonts larger than usual."

   This rule held up, it helped the user navigate easily.



**Task: How many people are ahead of you? What is your number?**

- Did they finish it?
   Yes!

- About how long it take
   About 7 seconds

- Where they hesitated, what they said, and anything that surprised you.

   He just paused a little bit for about 2 seconds to process what is going on in the UI and then proceeds to answer the questions correctly. 

   However when I asked a question "Ika pila ka sa linya?" He answered 1st (since number 1 is shown in the UI) but the real answer is 2nd. The number in the screen shows how many people are ahead not your actual position.

-Which of your persona's "Because …, my interface must …" rules held up, and which did not
   1) Because Rey is checking his queue position in Iligan before traveling to Cagayan de Oro, his queue position must the first thing he see and the biggest when opening the app. 
   2) Because Rey might be in class while checking for his queue position with a laptop, the interface must allow him to see his queue position very quickly with almost one tap to avoid instructor noticing him.

   This rules held up, the user quickly processed the UI and answered my question because the Queue position is the biggest part of the UI 

**Task: Pretend you are the staff member. Call the next person and mark them as served.**

-Did they finish it?
   Yes, with help

-About how long it take
   About 10 seconds

-Where they hesitated, what they said, and anything that surprised you.

  He hesitated when looking for the staff dashboard, so I helped him directly. I think this is acceptable because the database and login features are not yet implemented. Normally, the dashboard would be displayed based on the user's role. Staff users would automatically see the staff dashboard, eliminating the need to search for it manually.

-Which of your persona's "Because …, my interface must …" rules held up, and which did not

   Rules held up: Because winston is very busy, my interface must have a large and very noticeable button for notifying the next customer that it takes a second for winston to see it
   Rules did not : Because winston has blurry left eye and busy, my interface must only have a few buttons to minimize the risk of Winston accidentally pressing the wrong button while working.


**10b:MAKE ONE IMPROVEMENT**
One issue identified through self-review and usability testing is that users may mistake the highlighted, circled number on `MyPlace` (`ticket.html`) for their position in the queue. In reality, it represents the number of people ahead of them, meaning their actual position is the displayed number + 1.

I will keep this behavior but make the “People ahead of you” indicator more noticeable by improving its visibility, opacity, and contrast.

Overall, I found no major issues. Everything works as expected for a basic initial implementation.