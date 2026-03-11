import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { AnalyticsService } from './analytics.service';
import { CreateAnalyticsDto } from './dto/create-analytics.dto';
import { AnalyticsEntity } from './entity/analytics.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('analytics')
export class AnalyticsController {
  constructor(private readonly service: AnalyticsService) {}

  @Get()
  findAll(): Promise<AnalyticsEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<AnalyticsEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateAnalyticsDto): Promise<AnalyticsEntity> {
    return this.service.create(dto);
  }
}
