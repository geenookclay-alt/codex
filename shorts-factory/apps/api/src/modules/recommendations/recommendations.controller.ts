import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { RecommendationsService } from './recommendations.service';
import { CreateRecommendationsDto } from './dto/create-recommendations.dto';
import { RecommendationsEntity } from './entity/recommendations.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('recommendations')
export class RecommendationsController {
  constructor(private readonly service: RecommendationsService) {}

  @Get()
  findAll(): Promise<RecommendationsEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<RecommendationsEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateRecommendationsDto): Promise<RecommendationsEntity> {
    return this.service.create(dto);
  }
}
