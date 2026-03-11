import { Injectable } from '@nestjs/common';
import { LoginDto } from './dto/login.dto';

@Injectable()
export class AuthService {
  login(dto: LoginDto) {
    return { accessToken: `demo-token-${dto.email}`, role: 'admin' };
  }
}
