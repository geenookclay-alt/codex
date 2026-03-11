import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { AssetsService } from './assets.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('assets')
@UseGuards(JwtAuthGuard)
export class AssetsController {
  constructor(private readonly service: AssetsService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
