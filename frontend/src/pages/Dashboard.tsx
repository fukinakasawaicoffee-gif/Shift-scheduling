import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
} from '@mui/material';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  CalendarMonth as CalendarIcon,
  TrendingUp as TrendingUpIcon,
  ChevronRight as ChevronRightIcon,
} from '@mui/icons-material';
import { departmentAPI, employeeAPI, scheduleAPI } from '../services/api';
import { format, startOfMonth, endOfMonth } from 'date-fns';
import { ja } from 'date-fns/locale';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const currentMonth = new Date();
  const startDate = startOfMonth(currentMonth);
  const endDate = endOfMonth(currentMonth);

  // 部署数取得
  const { data: departments } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const response = await departmentAPI.getAll();
      return response.data;
    },
  });

  // 従業員数取得
  const { data: employees } = useQuery({
    queryKey: ['employees'],
    queryFn: async () => {
      const response = await employeeAPI.getAll();
      return response.data;
    },
  });

  // 今月のシフト数取得
  const { data: schedules } = useQuery({
    queryKey: ['schedules-current-month'],
    queryFn: async () => {
      const response = await scheduleAPI.getAll({
        start_date: format(startDate, 'yyyy-MM-dd'),
        end_date: format(endDate, 'yyyy-MM-dd'),
      });
      return response.data;
    },
  });

  const departmentCount = departments?.length || 0;
  const employeeCount = employees?.length || 0;
  const scheduleCount = schedules?.length || 0;
  const activeEmployeeCount = employees?.filter((e: any) => e.is_active)?.length || 0;

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        ダッシュボード
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {format(currentMonth, 'yyyy年M月', { locale: ja })}
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        {/* 統計カード */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              cursor: 'pointer',
              '&:hover': { boxShadow: 4 },
            }}
            onClick={() => navigate('/departments')}
          >
            <BusinessIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
            <Typography color="text.secondary" gutterBottom>
              部署数
            </Typography>
            <Typography variant="h3">{departmentCount}</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              cursor: 'pointer',
              '&:hover': { boxShadow: 4 },
            }}
            onClick={() => navigate('/employees')}
          >
            <PeopleIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />
            <Typography color="text.secondary" gutterBottom>
              従業員数
            </Typography>
            <Typography variant="h3">{employeeCount}</Typography>
            <Typography variant="caption" color="text.secondary">
              アクティブ: {activeEmployeeCount}名
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              cursor: 'pointer',
              '&:hover': { boxShadow: 4 },
            }}
            onClick={() => navigate('/schedule')}
          >
            <CalendarIcon sx={{ fontSize: 48, color: 'warning.main', mb: 1 }} />
            <Typography color="text.secondary" gutterBottom>
              今月のシフト
            </Typography>
            <Typography variant="h3">{scheduleCount}</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <TrendingUpIcon sx={{ fontSize: 48, color: 'info.main', mb: 1 }} />
            <Typography color="text.secondary" gutterBottom>
              稼働率
            </Typography>
            <Typography variant="h3">
              {employeeCount > 0 ? Math.round((scheduleCount / (employeeCount * 30)) * 100) : 0}%
            </Typography>
          </Paper>
        </Grid>

        {/* クイックアクション */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                クイックアクション
              </Typography>
              <Divider sx={{ my: 2 }} />
              <List>
                <ListItem
                  sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                  onClick={() => navigate('/departments')}
                >
                  <ListItemText
                    primary="部署を管理"
                    secondary="部署の追加・編集・削除"
                  />
                  <ChevronRightIcon />
                </ListItem>
                <ListItem
                  sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                  onClick={() => navigate('/employees')}
                >
                  <ListItemText
                    primary="従業員を管理"
                    secondary="従業員の追加・編集・削除"
                  />
                  <ChevronRightIcon />
                </ListItem>
                <ListItem
                  sx={{ cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}
                  onClick={() => navigate('/schedule')}
                >
                  <ListItemText
                    primary="シフトを自動生成"
                    secondary="AIによる最適なシフト作成"
                  />
                  <ChevronRightIcon />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* スタートガイド */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                スタートガイド
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body2" color="text.secondary" paragraph>
                1. <strong>部署を登録</strong>
                <br />
                部署管理画面から組織の部署を登録してください。
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                2. <strong>従業員を登録</strong>
                <br />
                従業員管理画面から各部署の従業員情報を登録してください。
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                3. <strong>シフトを生成</strong>
                <br />
                シフトカレンダー画面で自動生成ボタンをクリックして、最適なシフトを作成してください。
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small" onClick={() => navigate('/departments')}>
                はじめる
              </Button>
            </CardActions>
          </Card>
        </Grid>

        {/* 部署別統計 */}
        {departments && departments.length > 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                部署別従業員数
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Grid container spacing={2}>
                {departments.map((dept: any) => {
                  const deptEmployees = employees?.filter(
                    (e: any) => e.department_id === dept.id
                  ) || [];
                  return (
                    <Grid item xs={12} sm={6} md={4} key={dept.id}>
                      <Box
                        sx={{
                          p: 2,
                          border: 1,
                          borderColor: 'divider',
                          borderRadius: 1,
                          '&:hover': { bgcolor: 'action.hover', cursor: 'pointer' },
                        }}
                        onClick={() => navigate('/employees')}
                      >
                        <Typography variant="subtitle1" fontWeight="bold">
                          {dept.name}
                        </Typography>
                        <Typography variant="h4" color="primary">
                          {deptEmployees.length}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          従業員
                        </Typography>
                      </Box>
                    </Grid>
                  );
                })}
              </Grid>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default Dashboard;
