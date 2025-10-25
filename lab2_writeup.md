# Lab 2: Deploying My Note-Taking App to Vercel

## Introduction

For this lab, I was asked to deploy my note-taking application to Vercel, which is a platform that lets you host web applications in the cloud. This was actually quite challenging for me as someone who's still learning about web development, but I learned a lot along the way. In this writeup, I'll walk you through what I did, the problems I ran into, and what I learned from the experience.

## What I Built

I created a note-taking application that lets users create, edit, and organize their notes. The app has a nice interface inspired by Apple's design (which I really like), and it includes features like:

- Creating and editing notes
- Adding tags to organize notes
- Searching through notes
- Translating notes to different languages
- AI-powered note generation

## The Technology Stack I Used

Here's what I used to build this project:

**Frontend:**
- React with TypeScript (for the user interface)
- CSS for styling (I tried to make it look like Apple's website)
- HTML for the basic structure

**Backend:**
- Python with Flask (for the server that handles requests)
- SQLAlchemy (for working with databases)
- PostgreSQL (the database where notes are stored)

**Deployment:**
- Vercel (for hosting the app online)
- Supabase (for the database in the cloud)

## How I Built It - Step by Step

### Step 1: Setting Up the Database

The first challenge I faced was that Vercel doesn't work with regular file-based databases like SQLite (which I was using locally). I had to switch to PostgreSQL, which is a more powerful database that works well in the cloud.

I used Supabase to host my PostgreSQL database because it's free and easy to set up. I created scripts to help migrate my data from SQLite to PostgreSQL, which was actually pretty straightforward once I figured out how to do it.

### Step 2: Preparing for Vercel

Vercel works differently than running apps on my computer. I had to restructure my code so that:
- The frontend and backend could work together in the cloud
- The API routes were set up correctly
- The app could handle requests from anywhere on the internet

I created a `vercel.json` file that tells Vercel how to run my app, and I had to modify my Flask app to work with Vercel's serverless environment.

### Step 3: Making It Look Good

I spent a lot of time making the app look nice. I really like Apple's design style, so I tried to copy their approach:
- Used clean, simple fonts
- Picked colors that look professional
- Made sure everything is easy to read and use
- Added smooth animations when you hover over things

## A Really Important Lesson About Using AI

This might sound weird, but one of the most helpful things I learned during this project was to ask another AI to help me write better prompts for the AI I was working with. 

When I was trying to fix problems with my code, I would often write prompts like "fix this error" or "make this work better." But when I asked another AI to help me write a more detailed prompt, the results were much better. For example, instead of just saying "fix this error," I learned to say something like "I'm getting a database connection error when trying to deploy to Vercel. The error message says [specific error]. I'm using PostgreSQL with pg8000 adapter. Can you help me understand what's wrong and suggest a solution?"

The AI was able to give me much more helpful answers when I provided more context and was more specific about what I needed. This is definitely something I'll remember for future projects.

## The Deployment Process and Problems I Ran Into

### The Database Problem

The biggest issue I faced was getting the database to work with Vercel. At first, I tried using `psycopg2-binary`, which is a common way to connect Python to PostgreSQL databases. However, this didn't work because Vercel's environment couldn't compile this package properly.

After a lot of trial and error, I switched to `pg8000`, which is a pure Python PostgreSQL adapter that doesn't need to be compiled. This solved the database connection problem and my app could finally connect to the database in the cloud.

### The Current Problem: Can't Connect to the Backend

Even though I got the database working, I'm still having trouble with the frontend connecting to the backend. When I open the app in my browser, it shows an error message saying "Failed to load notes. Please check if the backend is running."

I've tried several things to fix this:
- Checked that the API routes are set up correctly
- Made sure the frontend is trying to connect to the right URL
- Verified that the backend code is working properly
- Tested the API endpoints directly

But I still can't figure out exactly what's wrong. The deployment shows as successful, but the frontend and backend aren't talking to each other properly. This is frustrating, but it's also a good learning experience about how complex web applications can be.

## What I Learned

This project taught me a lot about:
- How web applications work in the cloud
- The differences between local development and production deployment
- How databases work in serverless environments
- The importance of good error messages and debugging
- How to ask for help effectively (both from humans and AI)

## Conclusion

Even though I'm still working on fixing the connection between the frontend and backend, I'm proud of what I accomplished. I successfully deployed a web application to the cloud, set up a database, and learned a lot about modern web development. The process was challenging but also really rewarding.

I think the most important thing I learned is that building web applications is complex, and it's okay to run into problems. The key is to keep trying different solutions and not be afraid to ask for help when you get stuck.

## Next Steps

My immediate goal is to figure out why the frontend can't connect to the backend. Once I solve that, I want to:
- Add more features to the app
- Make it even more user-friendly
- Learn more about web development
- Maybe try deploying to other platforms to see how they compare

This project has definitely made me more interested in web development, and I'm excited to keep learning and building things.