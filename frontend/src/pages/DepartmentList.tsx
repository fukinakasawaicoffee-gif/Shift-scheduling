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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { departmentAPI } from '../services/api';
import { Department } from '../types';

const DepartmentList: React.FC = () => {
  const queryClient = useQueryClient();
  const [openDialog, setOpenDialog] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState<Department | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    max_regular_holidays_per_month: 8,
    max_consecutive_work_days: 6,
  });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });

  // データ取得
  const { data: departments, isLoading, error } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const response = await departmentAPI.getAll();
      return response.data;
    },
  });

  // 作成ミューテーション
  const createMutation = useMutation({
    mutationFn: (data: any) => departmentAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departments'] });
      handleCloseDialog();
      setSnackbar({ open: true, message: '部署を作成しました', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.response?.data?.detail || '作成に失敗しました', severity: 'error' });
    },
  });

  // 更新ミューテーション
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      departmentAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departments'] });
      handleCloseDialog();
      setSnackbar({ open: true, message: '部署を更新しました', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.response?.data?.detail || '更新に失敗しました', severity: 'error' });
    },
  });

  // 削除ミューテーション
  const deleteMutation = useMutation({
    mutationFn: (id: number) => departmentAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departments'] });
      setSnackbar({ open: true, message: '部署を削除しました', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.response?.data?.detail || '削除に失敗しました', severity: 'error' });
    },
  });

  const handleOpenDialog = (department?: Department) => {
    if (department) {
      setEditingDepartment(department);
      setFormData({
        name: department.name,
        code: department.code,
        description: department.description || '',
        max_regular_holidays_per_month: department.max_regular_holidays_per_month,
        max_consecutive_work_days: department.max_consecutive_work_days,
      });
    } else {
      setEditingDepartment(null);
      setFormData({
        name: '',
        code: '',
        description: '',
        max_regular_holidays_per_month: 8,
        max_consecutive_work_days: 6,
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingDepartment(null);
  };

  const handleSubmit = () => {
    if (editingDepartment) {
      updateMutation.mutate({ id: editingDepartment.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = (id: number) => {
    if (window.confirm('この部署を削除してもよろしいですか？')) {
      deleteMutation.mutate(id);
    }
  };

  if (isLoading) return <Container><Typography>読み込み中...</Typography></Container>;
  if (error) return <Container><Alert severity="error">エラーが発生しました</Alert></Container>;

  return (
    <Container maxWidth="lg">
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">部署管理</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          部署を追加
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>部署名</TableCell>
              <TableCell>部署コード</TableCell>
              <TableCell>説明</TableCell>
              <TableCell align="center">月の休日数</TableCell>
              <TableCell align="center">最大連続勤務日数</TableCell>
              <TableCell align="center">ステータス</TableCell>
              <TableCell align="center">操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {departments?.map((department: Department) => (
              <TableRow key={department.id}>
                <TableCell>{department.name}</TableCell>
                <TableCell>{department.code}</TableCell>
                <TableCell>{department.description}</TableCell>
                <TableCell align="center">{department.max_regular_holidays_per_month}日</TableCell>
                <TableCell align="center">{department.max_consecutive_work_days}日</TableCell>
                <TableCell align="center">
                  <Chip
                    label={department.is_active ? '有効' : '無効'}
                    color={department.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell align="center">
                  <IconButton
                    size="small"
                    color="primary"
                    onClick={() => handleOpenDialog(department)}
                  >
                    <EditIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => handleDelete(department.id)}
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
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingDepartment ? '部署を編集' : '部署を追加'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="部署名"
              fullWidth
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <TextField
              label="部署コード"
              fullWidth
              required
              value={formData.code}
              onChange={(e) => setFormData({ ...formData, code: e.target.value })}
            />
            <TextField
              label="説明"
              fullWidth
              multiline
              rows={3}
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
            <TextField
              label="月の通常休日数"
              type="number"
              fullWidth
              required
              value={formData.max_regular_holidays_per_month}
              onChange={(e) => setFormData({ ...formData, max_regular_holidays_per_month: parseInt(e.target.value) })}
            />
            <TextField
              label="最大連続勤務日数"
              type="number"
              fullWidth
              required
              value={formData.max_consecutive_work_days}
              onChange={(e) => setFormData({ ...formData, max_consecutive_work_days: parseInt(e.target.value) })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>キャンセル</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={!formData.name || !formData.code}
          >
            {editingDepartment ? '更新' : '作成'}
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

export default DepartmentList;
