import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Container,
  Typography,
  Paper,
  Button,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  Snackbar,
  CircularProgress,
} from '@mui/material';
import {
  AutoAwesome as AutoAwesomeIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { departmentAPI, employeeAPI, scheduleAPI, shiftPatternAPI } from '../services/api';
import { Department, Employee, Schedule, ShiftPattern } from '../types';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay } from 'date-fns';
import { ja } from 'date-fns/locale';

const ScheduleCalendar: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedDepartment, setSelectedDepartment] = useState<number | ''>('');
  const [selectedMonth, setSelectedMonth] = useState(format(new Date(), 'yyyy-MM'));
  const [openGenerateDialog, setOpenGenerateDialog] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });

  const monthDate = new Date(selectedMonth + '-01');
  const startDate = startOfMonth(monthDate);
  const endDate = endOfMonth(monthDate);
  const daysInMonth = eachDayOfInterval({ start: startDate, end: endDate });

  // 部署一覧取得
  const { data: departments } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const response = await departmentAPI.getAll();
      return response.data;
    },
  });

  // 従業員一覧取得
  const { data: employees } = useQuery({
    queryKey: ['employees', selectedDepartment],
    queryFn: async () => {
      if (!selectedDepartment) return [];
      const response = await employeeAPI.getAll(selectedDepartment);
      return response.data;
    },
    enabled: !!selectedDepartment,
  });

  // シフトパターン取得
  const { data: shiftPatterns } = useQuery({
    queryKey: ['shiftPatterns', selectedDepartment],
    queryFn: async () => {
      if (!selectedDepartment) return [];
      const response = await shiftPatternAPI.getAll(selectedDepartment);
      return response.data;
    },
    enabled: !!selectedDepartment,
  });

  // スケジュール取得
  const { data: schedules, isLoading, refetch } = useQuery({
    queryKey: ['schedules', selectedDepartment, selectedMonth],
    queryFn: async () => {
      if (!selectedDepartment) return [];
      const response = await scheduleAPI.getAll({
        department_id: selectedDepartment,
        start_date: format(startDate, 'yyyy-MM-dd'),
        end_date: format(endDate, 'yyyy-MM-dd'),
      });
      return response.data;
    },
    enabled: !!selectedDepartment,
  });

  // シフト自動生成ミューテーション
  const generateMutation = useMutation({
    mutationFn: (data: any) => scheduleAPI.generate(data),
    onSuccess: (response: any) => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] });
      setOpenGenerateDialog(false);
      setSnackbar({
        open: true,
        message: `シフトを自動生成しました（${response.data.schedules_created}件作成）`,
        severity: 'success',
      });
    },
    onError: (error: any) => {
      setSnackbar({
        open: true,
        message: error.response?.data?.message || 'シフト生成に失敗しました',
        severity: 'error',
      });
    },
  });

  const handleGenerateSchedule = () => {
    if (!selectedDepartment) {
      setSnackbar({ open: true, message: '部署を選択してください', severity: 'error' });
      return;
    }

    generateMutation.mutate({
      department_id: selectedDepartment,
      start_date: format(startDate, 'yyyy-MM-dd'),
      end_date: format(endDate, 'yyyy-MM-dd'),
      time_limit_seconds: 300,
    });
  };

  const getScheduleForEmployeeAndDate = (employeeId: number, date: Date): Schedule | undefined => {
    return schedules?.find(
      (s: Schedule) => s.employee_id === employeeId && isSameDay(new Date(s.date), date)
    );
  };

  const getShiftPatternById = (id: number): ShiftPattern | undefined => {
    return shiftPatterns?.find((sp: ShiftPattern) => sp.id === id);
  };

  const getShiftDisplay = (schedule: Schedule | undefined) => {
    if (!schedule) return '-';
    if (schedule.is_holiday) {
      return (
        <Chip
          label="休"
          size="small"
          color="default"
          sx={{ fontSize: '0.7rem', height: '20px' }}
        />
      );
    }
    const pattern = schedule.shift_pattern_id
      ? getShiftPatternById(schedule.shift_pattern_id)
      : null;
    if (pattern) {
      return (
        <Chip
          label={pattern.code}
          size="small"
          sx={{
            fontSize: '0.7rem',
            height: '20px',
            bgcolor: pattern.color_code || '#4ECDC4',
            color: 'white',
          }}
        />
      );
    }
    return '-';
  };

  if (!selectedDepartment) {
    return (
      <Container maxWidth="lg">
        <Typography variant="h4" gutterBottom>
          シフトカレンダー
        </Typography>
        <Paper sx={{ p: 3, mt: 3 }}>
          <Typography variant="body1" color="text.secondary">
            部署を選択してください
          </Typography>
          <FormControl sx={{ mt: 2, minWidth: 300 }}>
            <InputLabel>部署を選択</InputLabel>
            <Select
              value={selectedDepartment}
              label="部署を選択"
              onChange={(e) => setSelectedDepartment(e.target.value as number)}
            >
              {departments?.map((dept: Department) => (
                <MenuItem key={dept.id} value={dept.id}>
                  {dept.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">シフトカレンダー</Typography>
        <Box display="flex" gap={2} alignItems="center">
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>部署</InputLabel>
            <Select
              value={selectedDepartment}
              label="部署"
              onChange={(e) => setSelectedDepartment(e.target.value as number)}
            >
              {departments?.map((dept: Department) => (
                <MenuItem key={dept.id} value={dept.id}>
                  {dept.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
            type="month"
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            InputLabelProps={{ shrink: true }}
            label="対象月"
          />
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => refetch()}
          >
            更新
          </Button>
          <Button
            variant="contained"
            startIcon={<AutoAwesomeIcon />}
            onClick={() => setOpenGenerateDialog(true)}
            disabled={generateMutation.isPending}
          >
            {generateMutation.isPending ? 'Generated中...' : 'シフト自動生成'}
          </Button>
        </Box>
      </Box>

      {isLoading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer component={Paper}>
          <Table size="small" sx={{ minWidth: 1200 }}>
            <TableHead>
              <TableRow>
                <TableCell
                  sx={{
                    position: 'sticky',
                    left: 0,
                    bgcolor: 'background.paper',
                    zIndex: 1,
                    minWidth: 120,
                  }}
                >
                  従業員
                </TableCell>
                {daysInMonth.map((day) => (
                  <TableCell
                    key={day.toISOString()}
                    align="center"
                    sx={{ minWidth: 50, p: 0.5 }}
                  >
                    <Box>
                      <Typography variant="caption" display="block">
                        {format(day, 'M/d', { locale: ja })}
                      </Typography>
                      <Typography variant="caption" display="block" color="text.secondary">
                        {format(day, 'E', { locale: ja })}
                      </Typography>
                    </Box>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {employees?.map((employee: Employee) => (
                <TableRow key={employee.id}>
                  <TableCell
                    sx={{
                      position: 'sticky',
                      left: 0,
                      bgcolor: 'background.paper',
                      zIndex: 1,
                    }}
                  >
                    <Typography variant="body2" noWrap>
                      {employee.last_name} {employee.first_name}
                    </Typography>
                  </TableCell>
                  {daysInMonth.map((day) => {
                    const schedule = getScheduleForEmployeeAndDate(employee.id, day);
                    return (
                      <TableCell
                        key={`${employee.id}-${day.toISOString()}`}
                        align="center"
                        sx={{ p: 0.5 }}
                      >
                        {getShiftDisplay(schedule)}
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* シフト生成確認ダイアログ */}
      <Dialog open={openGenerateDialog} onClose={() => setOpenGenerateDialog(false)}>
        <DialogTitle>シフト自動生成</DialogTitle>
        <DialogContent>
          <Typography variant="body1" gutterBottom>
            {format(startDate, 'yyyy年M月', { locale: ja })}のシフトを自動生成しますか？
          </Typography>
          <Alert severity="warning" sx={{ mt: 2 }}>
            既存のシステム生成シフトは上書きされます
          </Alert>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              対象部署: {departments?.find((d: Department) => d.id === selectedDepartment)?.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              対象従業員: {employees?.length}名
            </Typography>
            <Typography variant="body2" color="text.secondary">
              期間: {format(startDate, 'yyyy/MM/dd')} 〜 {format(endDate, 'yyyy/MM/dd')}
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenGenerateDialog(false)}>キャンセル</Button>
          <Button
            onClick={handleGenerateSchedule}
            variant="contained"
            disabled={generateMutation.isPending}
          >
            {generateMutation.isPending ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1 }} />
                生成中...
              </>
            ) : (
              '生成開始'
            )}
          </Button>
        </DialogActions>
      </Dialog>

      {/* スナックバー */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ScheduleCalendar;
