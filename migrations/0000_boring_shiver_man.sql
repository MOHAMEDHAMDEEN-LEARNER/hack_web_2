CREATE TYPE "public"."notification_status" AS ENUM('draft', 'sent', 'failed');--> statement-breakpoint
CREATE TYPE "public"."notification_type" AS ENUM('mail', 'sms');--> statement-breakpoint
CREATE TYPE "public"."user_role" AS ENUM('admin', 'jury', 'applicant');--> statement-breakpoint
CREATE TABLE "applicant_sessions" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"session_token" varchar NOT NULL,
	"applicant_id" varchar NOT NULL,
	"expires_at" timestamp NOT NULL,
	"last_activity" timestamp DEFAULT now(),
	"created_at" timestamp DEFAULT now(),
	CONSTRAINT "applicant_sessions_session_token_unique" UNIQUE("session_token")
);
--> statement-breakpoint
CREATE TABLE "applicants" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"registration_id" varchar NOT NULL,
	"user_id" varchar,
	"name" text NOT NULL,
	"email" varchar NOT NULL,
	"mobile" varchar NOT NULL,
	"student_id" varchar NOT NULL,
	"course" text NOT NULL,
	"year_of_graduation" varchar NOT NULL,
	"college_name" text NOT NULL,
	"linkedin_profile" text,
	"status" text DEFAULT 'registered',
	"github_url" text,
	"submission_deadline" timestamp,
	"orientation_link" text,
	"orientation_sent" boolean DEFAULT false,
	"submission_enabled" boolean DEFAULT false,
	"selected_by" varchar,
	"selected_at" timestamp,
	"confirmation_token" varchar,
	"confirmed_at" timestamp,
	"event_day_registered" boolean DEFAULT false,
	"notes" text,
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now(),
	CONSTRAINT "applicants_registration_id_unique" UNIQUE("registration_id"),
	CONSTRAINT "applicants_mobile_unique" UNIQUE("mobile")
);
--> statement-breakpoint
CREATE TABLE "application_progress" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"applicant_id" varchar NOT NULL,
	"stage" varchar NOT NULL,
	"status" varchar NOT NULL,
	"description" text,
	"completed_at" timestamp,
	"created_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "competition_rounds" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar NOT NULL,
	"description" text NOT NULL,
	"start_time" timestamp,
	"end_time" timestamp,
	"max_participants" varchar,
	"current_participants" varchar DEFAULT '0',
	"total_colleges" varchar DEFAULT '0',
	"ideas_submitted" varchar DEFAULT '0',
	"prototypes_approved" varchar DEFAULT '0',
	"projects_approved" varchar DEFAULT '0',
	"total_invitees" varchar DEFAULT '0',
	"solutions_to_be_built" varchar DEFAULT '0',
	"status" varchar DEFAULT 'upcoming',
	"requirements" jsonb,
	"prizes" text[] DEFAULT '{}',
	"judge_ids" text[] DEFAULT '{}',
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "document_templates" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar NOT NULL,
	"description" text,
	"file_url" text,
	"file_type" varchar NOT NULL,
	"stage_id" varchar,
	"is_required" boolean DEFAULT true,
	"display_order" varchar DEFAULT '0',
	"is_active" boolean DEFAULT true,
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "event_settings" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"submission_deadline" timestamp,
	"orientation_link" text,
	"registration_enabled" boolean DEFAULT true,
	"submission_enabled" boolean DEFAULT false,
	"event_start_date" timestamp,
	"event_end_date" timestamp,
	"enable_emails" boolean DEFAULT true,
	"email_host" varchar,
	"email_port" varchar,
	"email_user" varchar,
	"email_pass" varchar,
	"from_email" varchar,
	"email_service" varchar DEFAULT 'gmail',
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "jury_members" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar NOT NULL,
	"email" varchar NOT NULL,
	"expertise" varchar NOT NULL,
	"company" varchar,
	"position" varchar,
	"status" varchar DEFAULT 'active',
	"assigned_applicants" text[] DEFAULT '{}',
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now(),
	CONSTRAINT "jury_members_email_unique" UNIQUE("email")
);
--> statement-breakpoint
CREATE TABLE "notifications" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"type" "notification_type" NOT NULL,
	"title" varchar NOT NULL,
	"description" text,
	"subject" varchar,
	"message" text,
	"to_emails" text[] DEFAULT '{}',
	"cc_emails" text[] DEFAULT '{}',
	"use_bulk_template" boolean DEFAULT false,
	"bulk_data" jsonb,
	"attachments" jsonb DEFAULT '[]'::jsonb,
	"status" "notification_status" DEFAULT 'draft',
	"sent_at" timestamp,
	"sent_count" varchar DEFAULT '0',
	"failed_count" varchar DEFAULT '0',
	"error_message" text,
	"created_by" varchar NOT NULL,
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "orientation_sessions" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"title" varchar NOT NULL,
	"description" text NOT NULL,
	"scheduled_time" timestamp NOT NULL,
	"meeting_link" varchar NOT NULL,
	"duration" varchar NOT NULL,
	"max_participants" varchar DEFAULT '100',
	"registered_count" varchar DEFAULT '0',
	"status" varchar DEFAULT 'scheduled',
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "otp_verifications" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"identifier" varchar NOT NULL,
	"otp" varchar NOT NULL,
	"purpose" varchar NOT NULL,
	"expires_at" timestamp NOT NULL,
	"verified" boolean DEFAULT false,
	"attempts" varchar DEFAULT '0',
	"created_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "payments" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"order_id" varchar NOT NULL,
	"applicant_id" varchar,
	"user_id" varchar,
	"amount" numeric(10, 2) NOT NULL,
	"currency" varchar DEFAULT 'INR' NOT NULL,
	"status" varchar NOT NULL,
	"payment_mode" varchar,
	"tracking_id" varchar,
	"bank_ref_no" varchar,
	"payment_type" varchar NOT NULL,
	"description" text,
	"billing_name" varchar NOT NULL,
	"billing_email" varchar NOT NULL,
	"billing_phone" varchar,
	"billing_address" text,
	"billing_city" varchar,
	"billing_state" varchar,
	"billing_zip" varchar,
	"billing_country" varchar DEFAULT 'India',
	"failure_message" text,
	"response_data" jsonb,
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now(),
	CONSTRAINT "payments_order_id_unique" UNIQUE("order_id")
);
--> statement-breakpoint
CREATE TABLE "project_submissions" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"applicant_id" varchar NOT NULL,
	"project_title" varchar NOT NULL,
	"description" text NOT NULL,
	"github_url" varchar NOT NULL,
	"live_url" varchar,
	"tech_stack" text[] NOT NULL,
	"submitted_at" timestamp DEFAULT now(),
	"jury_score" varchar,
	"jury_feedback" text,
	"status" varchar DEFAULT 'submitted',
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "sessions" (
	"sid" varchar PRIMARY KEY NOT NULL,
	"sess" jsonb NOT NULL,
	"expire" timestamp NOT NULL
);
--> statement-breakpoint
CREATE TABLE "stage_submissions" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"applicant_id" varchar NOT NULL,
	"stage_id" varchar NOT NULL,
	"github_url" text,
	"documents" jsonb DEFAULT '[]'::jsonb,
	"status" varchar DEFAULT 'draft',
	"submitted_at" timestamp,
	"reviewed_by" varchar,
	"reviewed_at" timestamp,
	"review_notes" text,
	"score" varchar,
	"feedback" text,
	"is_selected" boolean DEFAULT false,
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now()
);
--> statement-breakpoint
CREATE TABLE "submissions" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"applicant_id" varchar NOT NULL,
	"github_url" text NOT NULL,
	"submitted_at" timestamp DEFAULT now(),
	"reviewed_by" varchar,
	"reviewed_at" timestamp,
	"review_notes" text,
	"is_latest" boolean DEFAULT true
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" varchar PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"email" varchar,
	"password" varchar,
	"first_name" varchar,
	"last_name" varchar,
	"profile_image_url" varchar,
	"role" "user_role" DEFAULT 'applicant',
	"created_at" timestamp DEFAULT now(),
	"updated_at" timestamp DEFAULT now(),
	CONSTRAINT "users_email_unique" UNIQUE("email")
);
--> statement-breakpoint
ALTER TABLE "applicant_sessions" ADD CONSTRAINT "applicant_sessions_applicant_id_applicants_id_fk" FOREIGN KEY ("applicant_id") REFERENCES "public"."applicants"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "applicants" ADD CONSTRAINT "applicants_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "applicants" ADD CONSTRAINT "applicants_selected_by_users_id_fk" FOREIGN KEY ("selected_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "application_progress" ADD CONSTRAINT "application_progress_applicant_id_applicants_id_fk" FOREIGN KEY ("applicant_id") REFERENCES "public"."applicants"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "document_templates" ADD CONSTRAINT "document_templates_stage_id_competition_rounds_id_fk" FOREIGN KEY ("stage_id") REFERENCES "public"."competition_rounds"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "notifications" ADD CONSTRAINT "notifications_created_by_users_id_fk" FOREIGN KEY ("created_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "payments" ADD CONSTRAINT "payments_applicant_id_applicants_id_fk" FOREIGN KEY ("applicant_id") REFERENCES "public"."applicants"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "project_submissions" ADD CONSTRAINT "project_submissions_applicant_id_applicants_id_fk" FOREIGN KEY ("applicant_id") REFERENCES "public"."applicants"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "stage_submissions" ADD CONSTRAINT "stage_submissions_applicant_id_applicants_id_fk" FOREIGN KEY ("applicant_id") REFERENCES "public"."applicants"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "stage_submissions" ADD CONSTRAINT "stage_submissions_stage_id_competition_rounds_id_fk" FOREIGN KEY ("stage_id") REFERENCES "public"."competition_rounds"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "stage_submissions" ADD CONSTRAINT "stage_submissions_reviewed_by_users_id_fk" FOREIGN KEY ("reviewed_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "submissions" ADD CONSTRAINT "submissions_applicant_id_applicants_id_fk" FOREIGN KEY ("applicant_id") REFERENCES "public"."applicants"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "submissions" ADD CONSTRAINT "submissions_reviewed_by_users_id_fk" FOREIGN KEY ("reviewed_by") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "IDX_session_expire" ON "sessions" USING btree ("expire");