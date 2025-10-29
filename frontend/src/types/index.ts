export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface Department {
  id: number;
  name: string;
  code: string;
  description?: string;
  max_regular_holidays_per_month: number;
  max_consecutive_work_days: number;
  is_active: boolean;
}

export interface Employee {
  id: number;
  employee_code: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  department_id: number;
  hire_date?: string;
  birthday?: string;
  paid_leave_balance: number;
  summer_leave_balance: number;
  winter_leave_balance: number;
  birthday_leave_balance: number;
  is_active: boolean;
}

export enum ShiftType {
  EARLY = 'early',
  NORMAL = 'normal',
  LATE = 'late',
  NIGHT = 'night',
  OTHER = 'other',
}

export interface ShiftPattern {
  id: number;
  department_id: number;
  name: string;
  code: string;
  shift_type: ShiftType;
  start_time: string;
  end_time: string;
  work_hours: number;
  color_code?: string;
  is_active: boolean;
}

export interface Schedule {
  id: number;
  employee_id: number;
  shift_pattern_id?: number;
  date: string;
  is_holiday: boolean;
  holiday_type?: string;
  is_confirmed: boolean;
  is_published: boolean;
  generated_by_system: boolean;
  notes?: string;
}

export interface LeaveRequest {
  id: number;
  employee_id: number;
  leave_type: string;
  start_date: string;
  end_date: string;
  status: string;
  reason?: string;
  notes?: string;
}

export interface GenerateScheduleRequest {
  department_id: number;
  start_date: string;
  end_date: string;
  time_limit_seconds?: number;
}

export interface GenerateScheduleResponse {
  success: boolean;
  message: string;
  schedules_created: number;
  statistics: Record<string, any>;
}
