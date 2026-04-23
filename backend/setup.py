setup = ["""-- Users are handled by Supabase Auth automatically
-- This extends the auth user with extra profile info

create table profiles (
  id uuid references auth.users on delete cascade primary key,
  username text unique not null,
  level integer default 1,
  total_efficiency numeric default 0,
  exams_taken integer default 0,
  created_at timestamp default now()
);

create table papers (
  id uuid default gen_random_uuid() primary key,
  uploaded_by uuid references profiles(id),
  subject text,
  exam_board text,
  year integer,
  paper_number integer,
  total_marks integer,
  r2_filename text not null,
  created_at timestamp default now()
);

create table attempts (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references profiles(id),
  paper_id uuid references papers(id),
  score integer,
  total_marks integer,
  time_seconds integer,
  efficiency numeric generated always as
    (round((score::numeric / total_marks * 100) / (time_seconds::numeric / 60), 2)) stored,
  grade text,
  ai_feedback jsonb,
  created_at timestamp default now()
);

create table groups (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  join_code text unique not null,
  created_by uuid references profiles(id),
  created_at timestamp default now()
);

create table group_members (
  group_id uuid references groups(id) on delete cascade,
  user_id uuid references profiles(id) on delete cascade,
  role text default 'student',
  primary key (group_id, user_id)
);"""]


setup.append("""alter table profiles enable row level security;
alter table attempts enable row level security;
alter table papers enable row level security;

create policy "Users can view own profile"
  on profiles for select using (auth.uid() = id);

create policy "Users can update own profile"
  on profiles for update using (auth.uid() = id);

create policy "Users can view all papers"
  on papers for select using (true);

create policy "Users can insert own attempts"
  on attempts for insert with check (auth.uid() = user_id);

create policy "Users can view own attempts"
  on attempts for select using (auth.uid() = user_id);""")