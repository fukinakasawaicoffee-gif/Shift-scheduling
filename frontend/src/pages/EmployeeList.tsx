import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Container,
  Typography,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Box,
  Chip,
  Alert,
  Snackbar,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { employeeAPI, departmentAPI } from '../services/api';
import { Employee, Department } from '../types';

const EmployeeList: React.FC = () => {
  const queryClient = useQueryClient();
  const [openDialog, setOpenDialog] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [selectedDepartment, setSelectedDepartment] = useState<number | ''>('');
  const [formData, setFormData] = useState({
    employee_code: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    department_id: 0,
    hire_date: '',
    birthday: '',
    paid_leave_balance: 10,
    summer_leave_balance: 3,
    winter_leave_balance: 3,
    birthday_leave_balance: 1,
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });

  // 部署一覧取得
  const { data: departments } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const response = await departmentAPI.getAll();
      return response.data;
    },
  });

  // 従業員一覧取得
  const { data: employees, isLoading, error } = useQuery({
    queryKey: ['employees', selectedDepartment],
    queryFn: async () => {
      const response = await employeeAPI.getAll(selectedDepartment || undefined);
      return response.data;
    },
  });

  // 作成ミューテーション
  const createMutation = useMutation({
    mutationFn: (data: any) => employeeAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      handleCloseDialog();
      setSnackbar({ open: true, message: '従業員を作成しました', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.response?.data?.detail || '作成に失敗しました', severity: 'error' });
    },
  });

  // 更新ミューテーション
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      employeeAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      handleCloseDialog();
      setSnackbar({ open: true, message: '従業員を更新しました', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.response?.data?.detail || '更新に失敗しました', severity: 'error' });
    },
  });

  // 削除ミューテーション
  const deleteMutation = useMutation({
    mutationFn: (id: number) => employeeAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      setSnackbar({ open: true, message: '従業員を削除しました', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.response?.data?.detail || '削除に失敗しました', severity: 'error' });
    },
  });

  const handleOpenDialog = (employee?: Employee) => {
    if (employee) {
      setEditingEmployee(employee);
      setFormData({
        employee_code: employee.employee_code,
        first_name: employee.first_name,
        last_name: employee.last_name,
        email: employee.email || '',
        phone: employee.phone || '',
        department_id: employee.department_id,
        hire_date: employee.hire_date || '',
        birthday: employee.birthday || '',
        paid_leave_balance: employee.paid_leave_balance,
        summer_leave_balance: employee.summer_leave_balance,
        winter_leave_balance: employee.winter_leave_balance,
        birthday_leave_balance: employee.birthday_leave_balance,
      });
    } else {
      setEditingEmployee(null);
      setFormData({
        employee_code: '',
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        department_id: departments?.[0]?.id || 0,
        hire_date: '',
        birthday: '',
        paid_leave_balance: 10,
        summer_leave_balance: 3,
        winter_leave_balance: 3,
        birthday_leave_balance: 1,
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingEmployee(null);
  };

  const handleSubmit = () => {
    if (editingEmployee) {
      updateMutation.mutate({ id: editingEmployee.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = (id: number) => {
    if (window.confirm('この従業員を削除してもよろしいですか？')) {
      deleteMutation.mutate(id);
    }
  };

  const getDepartmentName = (departmentId: number) => {
    const dept = departments?.find((d: Department) => d.id === departmentId);
    return dept?.name || '-';
  };

  if (isLoading) return <Container><Typography>読み込み中...</Typography></Container>;
  if (error) return <Container><Alert severity="error">エラーが発生しました</Alert></Container>;

  return (
    <Container maxWidth="lg">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">従業員管理</Typography>
        <Box display="flex" gap={2}>
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>部署で絞り込み</InputLabel>
            <Select
              value={selectedDepartment}
              label="部署で絞り込み"
              onChange={(e) => setSelectedDepartment(e.target.value as number)}
            >
              <MenuItem value="">すべて</MenuItem>
              {departments?.map((dept: Department) => (
                <MenuItem key={dept.id} value={dept.id}>
                  {dept.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
          >
            従業員を追加
          </Button>
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>従業員コード</TableCell>
              <TableCell>氏名</TableCell>
              <TableCell>部署</TableCell>
              <TableCell>メール</TableCell>
              <TableCell align="center">有給残日数</TableCell>
              <TableCell align="center">ステータス</TableCell>
              <TableCell align="center">操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {employees?.map((employee: Employee) => (
              <TableRow key={employee.id}>
                <TableCell>{employee.employee_code}</TableCell>
                <TableCell>{employee.last_name} {employee.first_name}</TableCell>
                <TableCell>{getDepartmentName(employee.department_id)}</TableCell>
                <TableCell>{employee.email || '-'}</TableCell>
                <TableCell align="center">{employee.paid_leave_balance}日</TableCell>
                <TableCell align="center">
                  <Chip
                    label={employee.is_active ? '有効' : '無効'}
                    color={employee.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    size="small"
                    color="primary"
                    onClick={() => handleOpenDialog(employee)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => handleDelete(employee.id)}
                  >
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* 作成・編集ダイアログ */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingEmployee ? '従業員を編集' : '従業員を追加'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Box display="flex" gap={2}>
              <TextField
                label="従業員コード"
                fullWidth
                required
                value={formData.employee_code}
                onChange={(e) => setFormData({ ...formData, employee_code: e.target.value })}
              />
              <FormControl fullWidth required>
                <InputLabel>部署</InputLabel>
                <Select
                  value={formData.department_id}
                  label="部署"
                  onChange={(e) => setFormData({ ...formData, department_id: e.target.value as number })}
                >
                  {departments?.map((dept: Department) => (
                    <MenuItem key={dept.id} value={dept.id}>
                      {dept.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>
            <Box display="flex" gap={2}>
              <TextField
                label="姓"
                fullWidth
                required
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              />
              <TextField
                label="名"
                fullWidth
                required
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              />
            </Box>
            <Box display="flex" gap={2}>
              <TextField
                label="メールアドレス"
                type="email"
                fullWidth
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
              <TextField
                label="電話番号"
                fullWidth
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              />
            </Box>
            <Box display="flex" gap={2}>
              <TextField
                label="入社日"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
                value={formData.hire_date}
                onChange={(e) => setFormData({ ...formData, hire_date: e.target.value })}
              />
              <TextField
                label="誕生日"
                type="date"
                fullWidth
                InputLabelProps={{ shrink: true }}
                value={formData.birthday}
                onChange={(e) => setFormData({ ...formData, birthday: e.target.value })}
              />
            </Box>
            <Typography variant="subtitle2" sx={{ mt: 2 }}>休暇残日数</Typography>
            <Box display="flex" gap={2}>
              <TextField
                label="有給"
                type="number"
                fullWidth
                value={formData.paid_leave_balance}
                onChange={(e) => setFormData({ ...formData, paid_leave_balance: parseInt(e.target.value) })}
              />
              <TextField
                label="夏季休暇"
                type="number"
                fullWidth
                value={formData.summer_leave_balance}
                onChange={(e) => setFormData({ ...formData, summer_leave_balance: parseInt(e.target.value) })}
              />
              <TextField
                label="冬季休暇"
                type="number"
                fullWidth
                value={formData.winter_leave_balance}
                onChange={(e) => setFormData({ ...formData, winter_leave_balance: parseInt(e.target.value) })}
              />
              <TextField
                label="バースデー休暇"
                type="number"
                fullWidth
                value={formData.birthday_leave_balance}
                onChange={(e) => setFormData({ ...formData, birthday_leave_balance: parseInt(e.target.value) })}
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>キャンセル</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={!formData.employee_code || !formData.first_name || !formData.last_name || !formData.department_id}
          >
            {editingEmployee ? '更新' : '作成'}
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

export default EmployeeList;
