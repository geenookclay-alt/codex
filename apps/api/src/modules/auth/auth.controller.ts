import { Body, Controller, Post } from '@nestjs/common';
import { AuthService } from './auth.service';

@Controller('auth')
export class AuthController {
  constructor(private service: AuthService) {}
  @Post('login')
  login(@Body() body: { userId: string; role: string }) { return this.service.login(body.userId, body.role); }
}
