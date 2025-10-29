import React from 'react';
import { Container, Typography, Paper } from '@mui/material';

const DepartmentList: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        部署管理
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          部署管理機能（実装予定）
        </Typography>
      </Paper>
    </Container>
  );
};

export default DepartmentList;
