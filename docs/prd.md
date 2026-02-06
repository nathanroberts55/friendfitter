# Product Requirement Document: "The Bespoke Thread" (MVP)

**Date:** January 30, 2026

**Status:** Draft / Ready for Development

**Author:** AI Collaborator

---

## 1. Project Overview

**The Bespoke Thread** is a personalized production management system designed for "slow fashion" enthusiasts. The application allows a sewing hobbyist (Admin) to manage a library of thrifted fabric remnants and sewing patterns, matching them against the body measurements of a curated list of friends (Users).

### 1.1 Objectives

* **Centralize Data:** Create a single source of truth for friend measurements, fabric dimensions, and pattern requirements.
* **Automate Sizing Logic:** Eliminate manual cross-referencing by automatically filtering which friends fit which patterns given specific fabric constraints.
* **Maintain Surprise:** Ensure that gift recipients can manage their data without seeing the garments or fabrics being prepared for them.

---

## 2. User Personas

### 2.1 The Maker (Admin)

* **Role:** The tailor/sewer.
* **Needs:** To see a list of "Sewable Matches," manage fabric inventory, and track the progress of multiple projects.

### 2.2 The Recipient (Friend)

* **Role:** The person receiving the garment.
* **Needs:** A simple way to enter personal measurements and trust that their data is private.

---

## 3. Functional Requirements

### 3.1 Authentication & Privacy

* **OAuth Integration:** Users sign up/in using **Google** or **Discord** via `social-auth-app-django`.
* **Permission Tiers:** * **Admin:** Access to the "Matchmaker" dashboard, Fabric Inventory, and Pattern Library.
* **Users:** View and edit *only* their own Measurement Profile. They cannot see other users' data or the Admin's inventory.



### 3.2 Measurement Profile (Universal)

* **Data Points:** Bust/Chest, Waist, Hips, Shoulder Width, Inseam, and Total Height.
* **Visual Aid:** The entry form will include a reference diagram to ensure accurate placement of the measuring tape.

* **Metadata:** Profiles will display a "Last Updated" timestamp.

### 3.3 Fabric Inventory

* **Geometry:** Fabrics are measured by the **"Largest Usable Rectangle"** (Length  Width in inches).
* **Visuals:** One photo upload per fabric for visual identification.
* **Lifecycle:** Status moves from "Available" to "In Use" to "Scrap Pile" (Archive).

### 3.4 Pattern Library

* **Categorization:** Patterns must be tagged as **Top**, **Bottom**, or **Full Body**.
* **Sizing Matrix:** Admin manually enters the pattern's requirements grid:
* Size Number (e.g., 10, 12, 14).
* Body Measurement range for that size.
* Required Fabric Width vs. Required Fabric Length.


* **Visual Reference:** Upload a photo of the back of the pattern envelope for quick data entry reference.

---

## 4. The "Matchmaker" Engine (Strict Logic)

The system identifies a match only if the following conditions are met:

### Step A: Material Availability

The fabric rectangle must be large enough to accommodate the pattern's requirement for a specific size.


### Step B: Body Fit

The friend's measurements must fall within or below the pattern's size limits.

| Category | Required Checks for a "Strict Pass" |
| --- | --- |
| **Top** | Friend Chest & Shoulder Width  Pattern Size Limits |
| **Bottom** | Friend Waist & Hips  Pattern Size Limits |
| **Full Body** | All measurements (Bust, Waist, Hips, Shoulders)  Pattern Size Limits |

---

## 5. Technical Stack

| Component | Technology |
| --- | --- |
| **Framework** | Django (Python) |
| **Frontend** | Django Templates + Tailwind CSS + DaisyUI |
| **Auth** | Python Social Auth (Google/Discord) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Media** | Django File Storage (local or S3-compatible) |

---

## 6. User Interface (UI) Design

* **Admin Dashboard:** A "Matches" view showing a list of cards: *"You can make the [Pattern Name] for [Friend Name] using [Fabric Name]."*
* **Project Tracker:** A Kanban-style view (Planned  In Progress  Completed).
* **User Form:** A clean, mobile-responsive page for friends to submit measurements on the go.

---

## 7. Future Roadmap

* **Automatic OCR:** Using AI to scan pattern envelopes and auto-populate the sizing grid.
* **Yardage Converter:** Tool to convert fractional yards into inches automatically.
* **Ease Adjustment:** Moving from "Strict" matching to "Suggested" matching with ease-of-wear calculations.

---