# Airo Personal Workflow OS

## Goal

Turn Airo into a safe personal workflow assistant for daily productivity, non-sensitive finance tracking, Google Workspace output, Telegram intake, attachment handling, reminders, and monthly reports.

## Architecture Decision

Chosen architecture:

Full Database + Google Workspace as Output.

## Source of Truth

Local SQLite database first.

Google Workspace is used as:
- Sheets output
- Drive attachment storage
- Docs monthly reports
- Calendar reminders
- Gmail integration later

## Main Boundary

Airo must not access passwords, OTP, browser cookies, banking accounts, full Drive, or private secrets.

EarnsAI Pulse Trading remains fully separated.
